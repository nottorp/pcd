import urllib
import json

def query(tag):
    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=76d55f7653f69d24d85728b5e760d552&format=json&nojsoncallback=1&tags=" + tag
    remote_res = urllib.urlopen(url)
    remote_json = remote_res.read()
    parsed = json.loads(remote_json)
    return parsed

# {
# u'isfamily': 0,
# u'title': u'La vie est belle',
# u'farm': 2, u'ispublic': 1,
# u'server': u'1707',
# u'isfriend': 0,
# u'secret': u'4c98c22cf7',
# u'owner': u'29226759@N00',
# u'id': u'25049121326'
# }
# https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_[mstzb].jpg
def photo_record_to_url(attrs):
    res = "https://farm" + str(attrs["farm"]) + ".staticflickr.com/"
    res = res + str(attrs["server"]) + "/"
    res = res + str(attrs["id"]) + "_" +  str(attrs["secret"]) + "_m.jpg"
    return res

aa = query("rabbit")
print aa
print "Got", len(aa["photos"]["photo"]), "photos"

urllist = [photo_record_to_url(x) for x in aa["photos"]["photo"][:3]]

print urllist

