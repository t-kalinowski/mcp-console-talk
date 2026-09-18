#!/usr/bin/env python3
"""Exercise the deck's local YAML with harmless files in a disposable workspace.

Requires Python, PyYAML, and the installed mcp-console. Remote target examples
are parsed but are not launched. Network probes make HEAD requests to example.com.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--command', default='mcp-console')
    parser.add_argument('--out', type=Path, default=ROOT / 'captures/sandbox-validation.json')
    args = parser.parse_args()
    results = []
    configs = ROOT / 'examples/configs'
    workspace = {'config', 'permission-grants', 'private-inputs', 'temporary-storage',
                 'network-proxy', 'network-listener', 'proxy-options', 'enforcement-modes-1', 'enforcement-modes-2'}
    output_only = {'write-output', 'config-overrides'}
    with tempfile.TemporaryDirectory(prefix='console-talk-sandbox-') as temporary:
        root = Path(temporary).resolve()
        (root / '.agents/console').mkdir(parents=True)
        for name in ['output', 'data', 'secrets']:
            (root / name).mkdir()
            (root / name / 'input.txt').write_text('fixture\n')
        (root / '.env').write_text('FIXTURE_ONLY=true\n')
        for path in sorted(configs.glob('*.yaml')):
            config = yaml.safe_load(path.read_text())
            name = path.stem
            if 'target' in config:
                results.append({'config': path.name, 'status': 'not run',
                                'reason': 'Requires its configured remote host, image, or SBX template'})
                continue
            substitutions = {}
            proxy = config.get('sandbox', {}).get('proxy')
            if proxy:
                proxy['domains'] = {'example.com': 'allow', 'blocked.example.com': 'deny'}
                substitutions['proxy.domains'] = proxy['domains']
            (root / '.agents/console/config.yaml').write_text(yaml.safe_dump(config))
            expected = {
                'root_write': name in workspace,
                'output_write': name in workspace | output_only,
                'data_read': True,
                'data_write': name in workspace and name != 'private-inputs',
                'secret_read': name != 'private-inputs',
                'env_read': name != 'private-inputs',
            }
            # Check only synthetic files in this workspace; record OS refusals as values.
            code = '''from pathlib import Path
import json, os
result = {}
def probe(name, action):
    try:
        action()
        result[name] = True
    except PermissionError:
        result[name] = False
probe('root_write', lambda: Path('result.txt').write_text('fixture'))
probe('output_write', lambda: Path('output/result.txt').write_text('fixture'))
probe('data_read', lambda: Path('data/input.txt').read_text())
probe('data_write', lambda: Path('data/result.txt').write_text('fixture'))
probe('secret_read', lambda: Path('secrets/input.txt').read_text())
probe('env_read', lambda: Path('.env').read_text())
'''
            if name == 'environment-choice':
                code += "result['analysis_mode'] = os.environ['ANALYSIS_MODE']\nresult['inherited'] = 'TALK_FIXTURE_SENTINEL' in os.environ\n"
                expected.update(analysis_mode='interactive', inherited=False)
            if name == 'temporary-storage':
                code += "p = Path(os.environ['TMPDIR']) / 'scratch.txt'\np.write_text('scratch')\nresult['scratch_write'] = p.read_text() == 'scratch'\n"
                expected['scratch_write'] = True
            code += 'print(json.dumps(result))\n'
            env = {**os.environ, 'TALK_FIXTURE_SENTINEL':'fixture'}
            proc = subprocess.run([args.command, 'sandbox', '--', sys.executable, '-c', code],
                                  cwd=root, env=env, capture_output=True, text=True, timeout=45)
            entry = {'config': path.name, 'returncode': proc.returncode,
                     'expected': expected, 'stdout': proc.stdout, 'stderr': proc.stderr,
                     'substitutions': substitutions}
            results.append(entry)
            args.out.write_text(json.dumps(results,indent=2)+'\n')
            if name == 'knob-ownership' and sys.platform != 'linux':
                assert proc.returncode != 0 and 'linux_backend is supported only on Linux' in proc.stderr
                entry['status'] = 'expected platform rejection'
                print(f'{path.name}: Linux-only configuration rejected on {sys.platform}', flush=True)
                continue
            assert proc.returncode == 0, entry
            actual = json.loads(proc.stdout)
            assert actual == expected, (name, actual, expected)
            entry['status'] = 'passed'
            if name in {'default-sandbox', 'network-direct', 'network-proxy', 'network-listener'}:
                command = [args.command, 'sandbox', '--', '/usr/bin/curl', '-I', '--max-time', '15',
                           '--silent', '--show-error', '--fail', 'https://example.com']
                network = subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=45)
                entry['network'] = {'returncode':network.returncode,'stdout':network.stdout,'stderr':network.stderr}
                assert (network.returncode==0) == (name != 'default-sandbox'), entry
            if proxy:
                denied = subprocess.run([args.command,'sandbox','--','/usr/bin/curl','-I','--max-time','15',
                                         '--silent','--show-error','--fail','https://blocked.example.com'],
                                        cwd=root,capture_output=True,text=True,timeout=45)
                entry['denied_destination'] = {'returncode':denied.returncode,'stderr':denied.stderr}
                assert denied.returncode != 0 and '403' in denied.stderr, entry
                binding = subprocess.run([args.command,'sandbox','--',sys.executable,'-c',
                                          "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print('bound')"],
                                         cwd=root,capture_output=True,text=True,timeout=45)
                entry['local_binding'] = {'returncode':binding.returncode,'stdout':binding.stdout,'stderr':binding.stderr}
                assert (binding.returncode==0) == proxy['allowLocalBinding'], entry
            print(f'{path.name}: passed',flush=True)
        args.out.write_text(json.dumps(results,indent=2)+'\n')


if __name__ == '__main__':
    main()
