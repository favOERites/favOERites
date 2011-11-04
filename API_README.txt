####################################
########## Get your API key ########
####################################

1.) Login to OER bookmarks
2.) Go to 'Your Account'
3.) Your API key it will be listed in this section. 

####################################
############# General ##############
####################################

* format can be json or xml
* All call must pass api_key=YOUR_API_KEY and username=YOUR_USERNAME in order to authenticate. 
* Schema - http://127.0.0.1:8000/api/v1/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
* sets can be retrieved e.g. /api/v1/bookmark/set/1;3/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

####################################
############ Bookmark ##############
####################################

METHODS = [GET, POST, PUT, DELETE]

list 			-	http://127.0.0.1:8000/api/v1/bookmark/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
your bookmarks	-	http://127.0.0.1:8000/api/v1/mybookmark/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by id 			-	http://127.0.0.1:8000/api/v1/bookmark/<<BOOKMARK_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by filtering 	-	http://127.0.0.1:8000/api/v1/bookmark/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml&slug__startswith=a
set				- 	http://127.0.0.1:8000/api/v1/bookmark/set/1;2/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
schema 			-	http://127.0.0.1:8000/api/v1/bookmark/schema/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

## Examples - type (expected response) 

GET (201)		-	curl --dump-header - -H "Content-Type: application/json" -X GET "http://127.0.0.1:8000/api/v1/bookmark/<<BOOKMARK_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME"
POST (201)		-	curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"description": "My first OER bookmark.", "title": "A bookmark", "url":"http://www.medev.ac.uk"}' "http://127.0.0.1:8000/api/v1/bookmark/?api_key=YOUR_API_KEY&username=YOUR_USERNAME"
PUT (204)*		- 	curl --dump-header - -H "Content-Type: application/json" -X PUT --data '{"id": <<BOOKMARK_ID>>, "description": "My first OER bookmark.", "title": "A bookmark", "url":"http://www.medev.ac.uk/about/"}' "http://127.0.0.1:8000/api/v1/bookmark/<<BOOKMARK_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME"
DELETE (204)	-	curl --dump-header - -H "Content-Type: application/json" -X DELETE  "http://127.0.0.1:8000/api/v1/bookmark/<<BOOKMARK_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml"

* note: PUT must contain id 

####################################
############ USER ##################
####################################

METHODS = [GET]

list 			-	http://127.0.0.1:8000/api/v1/user/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by name			-	http://127.0.0.1:8000/api/v1/user/<<USERNAME>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
schema 			-	http://127.0.0.1:8000/api/v1/user/schema/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
profile			-	http://127.0.0.1:8000/api/v1/userprofile/<<USERNAME>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

####################################
############ Playlist ##############
####################################

METHODS = [GET, POST]

list 			-	http://127.0.0.1:8000/api/v1/playlist/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by id 			-	http://127.0.0.1:8000/api/v1/playlist/<<PLAYLIST_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by filtering 	-	http://127.0.0.1:8000/api/v1/playlist/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml&slug__startswith=a
set				- 	http://127.0.0.1:8000/api/v1/playlist/set/1;2/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
schema 			-	http://127.0.0.1:8000/api/v1/playlist/schema/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

## Examples - type (expected response) 

POST (201) 		-	curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"title": "A API playlist entry"}' "http://127.0.0.1:8000/api/v1/playlist/?api_key=YOUR_API_KEY&username=YOUR_USERNAME"

####################################
#### Bookmark/Playlist relation ####
####################################

METHODS = [GET, POST]

list 			-	http://127.0.0.1:8000/api/v1/playlistbookmarks/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

## examples 

POST (201)*		- 	curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"bookmark": "/api/v1/bookmark/<<BOOKMARK_ID>>/", "playlist":"/api/v1/playlist/<<PLAYLIST_ID>>/"}' "http://127.0.0.1:8000/api/v1/playlistbookmarks/?api_key=YOUR_API_KEY&username=YOUR_USERNAME"

* must contain bookmark and playlist uri


####################################
############## Vote ################
####################################

METHODS = [GET, POST, PUT, DELETE]

list 			-	http://127.0.0.1:8000/api/v1/vote/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by id 			-	http://127.0.0.1:8000/api/v1/vote/<<VOTE_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
schema 			-	http://127.0.0.1:8000/api/v1/vote/schema/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

## Examples (object must be bookmark or playlist uri, value must be 1 or -1)

POST (201) 		-	curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"value": "1","object": "/api/v1/bookmark/<<BOOKMARK_ID>>/"}' "http://127.0.0.1:8000/api/v1/vote/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml"
PUT (204)*		-	curl --dump-header - -H "Content-Type: application/json" -X PUT --data '{"value": "-1","object": "/api/v1/bookmark/<<BOOKMARK_ID>/", "id":<<VOTE_ID>>}' "http://127.0.0.1:8000/api/v1/vote/<<VOTE_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml"
DELETE (204)	-	curl --dump-header - -H "Content-Type: application/json" -X DELETE "http://127.0.0.1:8000/api/v1/vote/<<VOTE_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml"

* note: PUT must contain id 

####################################
############ Comment ###############
####################################

METHODS = [GET, POST, DELETE]

list 			-	http://127.0.0.1:8000/api/v1/comment/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
by id 			-	http://127.0.0.1:8000/api/v1/comment/<<COMMENT_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml
schema 			-	http://127.0.0.1:8000/api/v1/comment/schema/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml

## Examples 

POST (201) 		-	curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"comment": "Comment via the API", "object": "/api/v1/bookmark/21/"}' "http://127.0.0.1:8000/api/v1/comment/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml"
DELETE (204)	-	curl --dump-header - -H "Content-Type: application/json" -X DELETE "http://127.0.0.1:8000/api/v1/comment/<<COMMENT_ID>>/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml"	


####################################
############ Filtering #############
####################################

Standard

	* Standard - ['exact','iexact','startswith', 'istartswith', 'contains','icontains', 'endswith', 'iendswith']
	* Example - &title__startswith=abcd
	* if using one of the options prefixed with i this means a case-insensitive lookup will be used..

Relational

	* Same as standard but can span relations e.g. &user__username=james
	* complex example - http://127.0.0.1:8000/api/v1/user/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml&bookmarks__slug__icontains=OER - gets all users who have a bookmark that contains OER in the slug

See schema for specific options, e,g, http://127.0.0.1:8000/api/v1/bookmark/schema/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&format=xml for fields to filter by and filtering options.

####################################
############ Ordering #############
####################################

Playlist, Bookmark and User get request can be ordered, by all non-relational fields. Add order_by=field into url, examples:
	
	* http://127.0.0.1:8000/api/v1/user/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&order_by=username&format=xml
	* http://127.0.0.1:8000/api/v1/user/?api_key=YOUR_API_KEY&username=YOUR_USERNAME&order_by=username&format=xml (reversed)
	

 