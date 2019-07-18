import yaml
import os
import base64
import errno

config_path = './config'
site_path = './site'

def checkNode(obj):
    return obj['host'] != None and obj['password'] != None and obj['encryption'] != None and obj['obfs'] != None

# ssr://base64(host:port:protocol:method:obfs:base64pass/?obfsparam=base64param&protoparam=base64param&remarks=base64remarks&group=base64group&udpport=0&uot=0)
def buildURL(node, group):
    str = '{host}:{port}:{protocal}:{method}:{obfs}:{password}/?obfsparam={obfs_param}&protoparam={protocal_param}&remarks={note}&group={group}&udpport={udp}&uot={uot}'.format(
        host=node['host'],
        port=node['port'],
        protocal=node['protocal'],
        method=node['encryption'],
        obfs=node['obfs'],
        password=base64.urlsafe_b64encode(node['password'].encode()).decode(),
        obfs_param=base64.urlsafe_b64encode(node['obfs_param'].encode()).decode(),
        protocal_param=base64.urlsafe_b64encode(node['protocal_param'].encode()).decode(),
        note=base64.urlsafe_b64encode(node['note'].encode()).decode(),
        group=base64.urlsafe_b64encode(group.encode()).decode(),
        udp=node['udp'],
        uot=node['uot']
    )

    return 'ssr://{}'.format(base64.urlsafe_b64encode(str.encode()).decode())

def buildCollection(nodes, group):
    ls = []
    for node in nodes:
            if (checkNode(node)):
                ls.append(buildURL(node, group))
            else:
                print('Err: Missing Params')

    return base64.urlsafe_b64encode(' '.join(ls).encode()).decode()

# main
if not os.path.exists(site_path):
    os.makedirs(site_path)

public = []

files = os.listdir(config_path)

for file in files:
    path = os.path.join(config_path, file)
    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]
    if os.path.isfile(path):
        with open(path) as f:
            data = yaml.load(f)
            generated = '{}.txt'.format(filename)
            str = buildCollection(data['nodes'], data['name'])
            with open(os.path.join(site_path, generated),"w+") as w:
                w.write(str)
            if (data['public'] == True):
                public.append({'name': data['name'], 'filename': generated})

with open(os.path.join(site_path, 'index.html'), 'w+') as w:
    for f in public:
        w.write('<p><a href="{}">{}</a></p>'.format(f['filename'], f['name']))