from flask import Flask, jsonify ,request  
from urllib2 import Request, urlopen, URLError
import json 
import oauth2 as oauth

# Initialize the Flask application
#winureze@vpsorg.top
app = Flask(__name__)

API_Key =  "rX2mTlTJcRQznOimo3ACbUZrh" ; 
API_Secret = "nGL9vtY9guZeS6v4PXxRUmaxzWgqHG38iiEWqHjLEyIpWg5kxD" 
Access_Token ="1713417284-RnYkTiz5o14rnuPW0S7TNN3p1CluMLT55t9PT6n"
Access_Token_Secret ="09CLDBBVS9ZEok50hTprwGLMWk7L1ez7bHwPk2kfS4c74" 

# Define a route for the default URL, which loads the form
@app.route('/', methods= ['GET'])
def test():
	# print request.args.get("q")
	return  jsonify({'message': 'it works'})

# search using apis 
@app.route('/search', methods= ['POST' , 'GET'])
def search():
	# inp = request.json['query']
	inp = request.args.get("q")
	inpu =  inp.split(' ')
	inp = "" 
	for a in inpu : 
		inp = inp + a + "+"
	inp = inp[:len(inp)-1]; 	
	# inp = "the+dark+knight"
	# print inp
	# inpu  = inp.split[" "] ;
	# print inpu 

	url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyDe-kSqgLS-GZEmWGtORA_cK7jCTcUKxRs&cx=017576662512468239146:omuauf_lfve&q="
	url += inp 
	print url 
	req = Request(url)
	#get google results  
	try:
		response = urlopen(req)
		kit = response.read()
		google = json.loads(kit)
		gresult = { "link" : google["items"][0]["formattedUrl"], "text" : google["items"][0]["htmlSnippet"]}
		# result = {"google" : gresult} 
		#get duckduckgo results 
		url1 = "http://api.duckduckgo.com/?q="+ inp+ "&format=json" ;
		try: 
			dresp = urlopen(Request(url1)) ; 
			dkit = dresp.read();
			djs = json.loads(dkit)
			dresult = {"link": djs['RelatedTopics'][0]['FirstURL'] , "text" : djs['RelatedTopics'][0]['Text'] } 
			# get twitter results 
			url2 ="https://api.twitter.com/1.1/search/tweets.json?q="+ inp
			consumer = oauth.Consumer(key= API_Key , secret = API_Secret); 
			access_token =	oauth.Token(key= Access_Token , secret = Access_Token_Secret) ;
			client = oauth.Client(consumer , access_token) ; 
			tresp ,data = client.request(url2)
			tweets = json.loads(data) ; 
			# print data

			idd =  tweets['statuses'][0]['id']
			link = "https://twitter.com/statuses/"+ str(idd) 
			text = tweets['statuses'][0]['text']
			tresult = {"link": link , "text" : text}
			# print tresult
			ans = {"query" : inp , "results" : {"google": gresult , "duckduckgo" : dresult , "twitter": tresult}}; 
			# print ans 
			return jsonify(ans)  
		except URLError , e :
			print 'DuckDuckGo api not working:', e  ; 	 
			return  jsonify({'Error': 'Duck Api'})	; 		
	except URLError, e:
	  	print 'Google api not working:', e ; 
		return  jsonify({'Error': 'google Api'})


# search()
# test()
# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("8080")
  )
