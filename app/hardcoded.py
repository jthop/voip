systems = {
    1: {
        'domain': 'fon.ee', 
        'ntp1': '10.10.10.24', 
        'ntp2': '10.10.10.25', 
        'syslog': '10.10.10.10', 
        'default_wallpaper': 'http://pnp.fon.ee/static/wallpaper/mode14.png', 
        'boot_text': 'welcome to fon.ee', 
        'directory': {
            'url': 'http://pnp.fon.ee/cp/dir.xml', 
            'name': 'Directory'
            }, 
        'page_groups': ['pggrp=224.168.168.168:34560;name=All;num=801;listen=yes;pri=3;codec=g722'], 
        'time': {
            'time_zone': 'GMT-06:00', 
            'dst_enable': True, 
            'dst_rule': 'start=3/-2/7/2;end=11/-2/7/2;save=1'
            }, 
        'provision': {
            'rule': 'https://pnp.fon.ee/cp/conf/$MAU.xml', 
            'ruleB': None, 
            'ruleC': None, 
            'ruleD': None, 
            'dhcp_options_V4': '66,160,159,150',
            'dhcp_options_V6': '17,160,159',
            'gppA': '<RESERVED>', 
            'gppC': '<RESERVED>', 
            'gppD': '<RESERVED>', 
            'gppE': '<RESERVED>', 
            'gppF': '<RESERVED>', 
            'gppG': '<RESERVED>', 
            'gppH': '<RESERVED>', 
            'gppI': '<RESERVED>', 
            'gppJ': None, 
            'gppK': None,
            'gppL': None, 
            'gppM': None, 
            'gppN': None,
            'gppO': None, 
            'gppP': None
        }, 
        'report': '[--status]http://pnp.fon.ee/config-mpp-status.xml [--delta]http://pnp.fon.ee/config-mpp-delta.xml'
    }
}

models = {
    'CP-8841-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 10, 
            'video': False, 
            'wifi': False, 
            'bluetooth': True
        }
    }, 
    'CP-8851-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 10, 
            'video': False, 
            'wifi': False, 
            'bluetooth': True, 
            'units': 2, 
            'kem': {
                'model': 'CP-8800-Audio', 
                'buttons': 28, 'units': 2
            }
        }
    }, 
    'CP-8861-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 10, 
            'video': False, 
            'wifi': False, 
            'bluetooth': True, 
            'units': 3, 
            'kem': {
                'model': 'CP-8800-Audio', 
                'buttons': 28, 
                'units': 3
            }
        }
    }, 
    'CP-8845-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 10, 
            'video': True,
            'wifi': False, 
            'bluetooth': False
        }
    }, 
    'CP-8865-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 10, 
            'video': True, 
            'wifi': True, 
            'bluetooth': True, 
            'kem': {
                'model': 'CP-8800-Video', 
                'buttons': 36, 
                'units': 3
            }
        }
    }, 
    'CP-7821-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 2, 
            'video': False, 
            'wifi': False, 
            'bluetooth': False
        }
    }, 
    'CP-7841-3PCC': {
        'template': 'cisco_v1.xml', 
        'features': {
            'buttons': 4, 
            'video': False, 
            'wifi': False, 
            'bluetooth': False
        }
    }
}
