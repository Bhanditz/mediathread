#

all = [
    {'title':'YouTube',
     'metadata':{'description':
                     "The largest collection of video on the web, where you can also upload video yourself.",
                 'required':['flash'],
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://www.youtube.com/',
                   },
            'archive':{'label':'archive',
                       'url':'http://www.youtube.com/',
                       },
            'thumb':{'label':'thumb',
                     'url':'/site_media/img/youtube_logo.jpg',
                     },
            },
     },
    {'title':'WGBH OpenVault: The Vietnam Collection',
     'metadata':{'description':
                     "Vietnam: A Television History was a landmark documentary series produced by WGBH. This collection contains most of the materials gathered and created for the 1983 series, as well as additional Vietnam-related materials from the WGBH archive.",
                 'required':['flash'],
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://openvault.wgbh.org/catalog/org.wgbh.mla:Vietnam',
                   },
            'archive':{'label':'archive',
                       'url':'http://openvault.wgbh.org/catalog/org.wgbh.mla:Vietnam',
                       },
            'thumb':{'label':'thumb',
                     'url':'http://ccnmtl.columbia.edu/projects/mediathread/skins/vietnam//img/bvault_bug.jpg',
                     },
            },
     },
    {'title':'Flickr',
     'metadata':{'description':
                     "One of the largest collections of user-uploaded images on the web."
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://www.flickr.com/',
                   },
            'archive':{'label':'archive',
                       'url':'http://www.flickr.com/',
                       },
            'thumb':{'label':'thumb',
                     'url':'/site_media/img/flickr_logo.png',
                     },
            },
     },
    {'title':'Digital Tibet',
     'metadata':{'description':
                     "An advanced, searchable repository of Tibetan objects from several collections including the Rubin Museum, Himalayan Art Resources, and the Starr East Asian Library."
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://digitaltibet.ccnmtl.columbia.edu/',
                   },
            'archive':{'label':'archive',
                       'url':'http://digitaltibet.ccnmtl.columbia.edu/',
                       },
            'thumb':{'label':'thumb',
                     'url':'http://digitaltibet.ccnmtl.columbia.edu/sites/digitaltibet.ccnmtl.columbia.edu/themes/tibetan/ccnmtl_images/portfolio_image.jpg',
                     },
            'bookmarklet_button':{'label':'bookmarklet_button',
                                  'url':'/site_media/img/analyze_button.jpg',
                                  },
            },
     },
    {'title':'Vanderbilt Television News Archive',
     'metadata':{'description':
                     """This archive has been recording, preserving and providing access to television news broadcasts of the national networks since August 5, 1968.	NBC footage in the archive is viewable online.

INSTRUCTIONS
Online video is in RealMedia format.  If  you are unable to view it, install the plugin from http://www.real.com/ 

Find an online video in the database (indicated by a camera icon), and click the 'view video' button.  A window will pop up and the video will play; click on the video's 'permalink' to open it in your main browser window and close the pop-up.  

Then click the Analyze w/Mediathread bookmarklet in your browser to bring the video into Mediathread.  You will be given the option at this point to give the video a descriptive title.
""",
                 'required':['realplayer'],
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://tvnews.vanderbilt.edu/',
                   },
            'archive':{'label':'archive',
                       'url':'http://tvnews.vanderbilt.edu/',
                       },
            'thumb':{'label':'thumb',
                     'url':'http://tvnews.vanderbilt.edu.ezproxy.cul.columbia.edu/images/vcrest.gif',
                     },
            },
     },
    {'title':'The Tibetan & Himalayan Library',
     'metadata':{'description':
                     "Includes murals from the Meru Nyingpa (rme ru rnying pa) Monastery which is located in the Barkor (bar skor) area at the heart of the old city of Lhasa (lha sa), just east of the famed Jokhang (jo khang) Temple."
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://thlib.org/places/monasteries/meru-nyingpa/murals/',
                   },
            'archive':{'label':'archive',
                       'url':'http://thlib.org/places/monasteries/meru-nyingpa/murals/',
                       },
            'thumb':{'label':'thumb',
                     'url':'http://thlib.org/places/monasteries/meru-nyingpa/murals/preview/mnmural01.jpg',
                     },
            },
     },
    {'title':'Shakespeare Performance in Asia',
     'metadata':{'description':
                     "The MIT Shakespeare Electronic Archive presents an extensive collection of videos of Asian Shakespeare performances. Here you will also find interactive maps and timelines, interviews, biographies of directors and actors, for understanding intercultural Shakespeare.",
                 'required':['flash','quicktime'],
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://web.mit.edu/shakespeare/asia/',
                   },
            'archive':{'label':'archive',
                       'url':'http://web.mit.edu/shakespeare/asia/',
                       },
            'thumb':{'label':'thumb',
                     'url':'http://web.mit.edu/shakspere/sia/wmv_images/wmv_images_sm/mac_tian.jpg',
                     },
            },
     },
    {'title':'ARTstor',
     'metadata':{'description':
                     """A nonprofit digital library of more than one million images in the arts, architecture, humanities, and social sciences.

INSTRUCTIONS
You do not need to log in to ARTstor to bring images into Mediathread. 

When you find an image you want to analyze in an ARTstor collection, click on its title (underneath its thumbnail).  A pop-up window will display the image's metadata.  At this point, click on the Analyze w/Mediathread bookmarklet in your main browser window.  The image will then load in Mediathread.
""",
                 'required':['flash'],
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'http://library.artstor.org/library/welcome.html',
                   },
            'archive':{'label':'archive',
                       'url':'http://library.artstor.org/library/welcome.html',
                       },
            'thumb':{'label':'thumb',
                     'url':'http://library.artstor.org/library/g-artstor-logo.gif',
                     },
            },
     },

]

template =     {'title':'',
     'metadata':{'description':
                     ""
                 },
     'sources':{
            'url':{'label':'url',
                   'url':'',
                   },
            'archive':{'label':'archive',
                       'url':'',
                       },
            'thumb':{'label':'thumb',
                     'url':'',
                     },
            },
     },
