import os, re

with open('index.html', 'r') as f:
    content = f.read()

# Replace the QR code URL with local image
old = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://rdstudiohub.github.io/Basateen-Al-Dammam/&margin=10'
new = 'qr_big.png'

content = content.replace(old, new)

# Also update the footer map link
old_map = 'https://maps.google.com/?q=Basateen+Al+Dammam+Restaurant'
new_map = 'https://maps.google.com/?q=Basateen+Al+Dammam+Restaurant+%D8%A7%D9%84%D8%AF%D9%85%D8%A7%D9%85'

content = content.replace(old_map, new_map)

with open('index.html', 'w') as f:
    f.write(content)

print("✅ index.html updated with local QR code")
print(f"Size: {len(content)}")
