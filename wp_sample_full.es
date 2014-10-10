Resource -> ttl:300
    Rule config.init -> comment:"Set up some default system values"
        Prerequisite -> priority:-10000
            Defmac PROCESS_VERY_EARLY -> value:-10000
            Defmac PROCESS_EARLY -> value:-1000
            Defmac PROCESS_NORMAL -> value:0
            Defmac PROCESS_LATE -> value:1000
            Defmac PROCESS_VERY_LATE -> value:10000
            
    Rule Hostname.setup ->
        Prerequisite ->
            Defmac varHost -> value:"booksplusplus.wordpress.com"

    Rule root.media_wordpress -> comment:"Wordpress Various external references" match-path:"/_fwpcom/*"
        SetCache -> aggressive:true cookies:ignore insecure:true
        
        Compose default ->
            Fetch -> type:proxy
                Script -> value:"request.host = request.path.split('/')[2]; request.path = request.path.replace('/_fwpcom/' + request.host, '');"
    
    Rule root.login_wordpress -> comment:"Wordpress Login Area" match-path:"/wp-login.php*"
        Apply Hostname.setup ->
        
        SetCache -> aggressive:true cookies:no-cache insecure:false
        
        Compose ->
            Fetch -> type:proxy
            Script -> value:"var temp = request.url; temp = temp.replace(request.host, macros.varHost); if (request.method == 'POST') { temp = temp.replace('http://', 'https://'); } request.url = temp;"
            Replace -> regex:"http://s[0-9]\.wp\.com" value:"/cdn"
            Replace -> regex:"https?://[a-zA-Z0-9]*?\.wordpress\.com/wp-admin" value:"http://wordpress.com/wp-admin"
            Replace -> regex:"https?://[a-zA-Z0-9]*?\.wordpress\.com/" value:"/"

    Rule -> comment:"Proxy, Compress and Adjust the wordpress site" match-host:"*"
        Apply Hostname.setup -> required:false
        SetCache -> aggressive:true cookies:ignore insecure:true
        
        Compose -> priority:PROCESS_NORMAL
            Fetch -> type:proxy
                Set -> host:varHost
            Deliver -> if:"document.contentType != 'text/html' || document.responseCode != 200"

            Modify -> xpath:"//img[@src]|//script[@src]|//a[@href]|//link[@href]"
                Attr replace -> name:"src" value:"http://" with:"/_fwpcom/"
                Attr replace -> name:"href" value:"http://" with:"/_fwpcom/"

            Replace -> regex:"http://${varHost}/" value:"/"
            Replace -> regex:"http://www.${varHost}/" value:"/"
            Replace -> regex:"http://${varHost}" value:"/"
            Replace -> regex:"http://www.${varHost}" value:"/"
            Replace -> regex:"http:\\/\\/${varHost}\\/" value:"/"