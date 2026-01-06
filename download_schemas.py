"""Script to download BatteryPass JSON schemas - handles UTF-16 LE BOM encoding."""
import urllib.request
import ssl
import os

# SSL context for corporate proxies
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

schemas = [
    ('CarbonFootprintForBatteries-schema.json', 
     'https://raw.githubusercontent.com/batterypass/BatteryPassDataModel/main/BatteryPass/io.BatteryPass.CarbonFootprint/1.2.0/gen/CarbonFootprintForBatteries-schema.json'),
    ('Circularity-schema.json', 
     'https://raw.githubusercontent.com/batterypass/BatteryPassDataModel/main/BatteryPass/io.BatteryPass.Circularity/1.2.0/gen/Circularity-schema.json'),
    ('MaterialComposition-schema.json', 
     'https://raw.githubusercontent.com/batterypass/BatteryPassDataModel/main/BatteryPass/io.BatteryPass.MaterialComposition/1.2.0/gen/MaterialComposition-schema.json'),
    ('PerformanceAndDurability-schema.json', 
     'https://raw.githubusercontent.com/batterypass/BatteryPassDataModel/main/BatteryPass/io.BatteryPass.Performance/1.2.0/gen/PerformanceAndDurability-schema.json'),
    ('Labeling-schema.json', 
     'https://raw.githubusercontent.com/batterypass/BatteryPassDataModel/main/BatteryPass/io.BatteryPass.Labels/1.2.0/gen/Labeling-schema.json'),
    ('SupplyChainDueDiligence-schema.json', 
     'https://raw.githubusercontent.com/batterypass/BatteryPassDataModel/main/BatteryPass/io.BatteryPass.SupplyChainDueDiligence/1.2.0/gen/SupplyChainDueDiligence-schema.json'),
]

base_path = 'src/NMIS_Ecopass/models/BatteryPass/schemas'

for filename, url in schemas:
    filepath = os.path.join(base_path, filename)
    print(f'Downloading {filename}...')
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as response:
        data = response.read()
        
        # Handle UTF-16 LE with BOM (starts with \xff\xfe)
        if data.startswith(b'\xff\xfe'):
            content = data.decode('utf-16-le')
        elif data.startswith(b'\xfe\xff'):
            content = data.decode('utf-16-be')
        else:
            content = data.decode('utf-8')
        
        # Write as UTF-8
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f'  Saved: {filepath}')

print('Done!')
