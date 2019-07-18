import yaml
import os
import base64
import urllib.parse

config_path = './config'
site_path = './site'

def base64encode(str):
    return base64.urlsafe_b64encode(str.encode()).decode() #.replace("=","") don't remove padding

def checkNode(obj):
    return obj['host'] != None and obj['password'] != None and obj['encryption'] != None and obj['obfs'] != None

# ssr://base64(host:port:protocol:method:obfs:base64pass/?obfsparam=base64param&protoparam=base64param&remarks=base64remarks&group=base64group&udpport=0&uot=0)
def buildSSRURL(node, group):
    str = '{host}:{port}:{protocal}:{method}:{obfs}:{password}/?obfsparam={obfs_param}&protoparam={protocal_param}&remarks={note}&group={group}&udpport={udp}&uot={uot}'.format(
        host=node['host'],
        port=node['port'],
        protocal=node['protocal'],
        method=node['encryption'],
        obfs=node['obfs'],
        password=base64encode(node['password']),
        obfs_param=base64encode(node['obfs_param']),
        protocal_param=base64encode(node['protocal_param']),
        note=base64encode(node['note']),
        group=base64encode(group),
        udp=node['udp'],
        uot=node['uot']
    )

    return 'ssr://{}'.format(base64encode(str))

# ss://YmYtY2ZiOnRlc3Q@192.168.100.1:8888/?plugin=url-encoded-plugin-argument-value&unsupported-arguments=should-be-ignored#Dummy+profile+name
def buildSSURL(node, group):
    if node['protocal'] == 'plain':
        return 'ss://{info}@{host}:{port}/#{note}'.format(
            info=base64encode('{method}:{password}'.format(
                password=node['password']
                method=node['encryption']
            ))
            host=node['host']
            note=urllib.parse.quote(node['note'])
        )
    else: 
        return ''

def buildCollection(nodes, group):
    ssr = []
    # ss = []
    for node in nodes:
            if (checkNode(node)):
                ls.append(buildSSRURL(node, group))
                # ss_str = buildSSURL(node, group)
                # if ss_str != '':
                #     ss.append(ss_str)
            else:
                print('Err: Missing Params')

    return base64encode(' '.join(ls))

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