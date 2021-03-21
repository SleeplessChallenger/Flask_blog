<h2>Some memos about RESTful things in Flask</h2>

1. Rich Internet Applications (RIAs) - when business logic of web applications is moved as much as possible to client's side.
	Why API? In the aforewritten case the server becomes API or web service. + main and sole task of server is to provide the client application with data retrieval and storage services. 

	Representational State Transfer (REST) is the most popular so-called protocol via which
	RIAs communicate with web service/API.


2. Resources are everything in REST. They can be considered as: posts, comments, users etc
   Each resource must have a unique identifier that represents it
   When working with HTTP, identifiers for resources are URLs: URL /api/posts/12345

3. A collection of all the resources in a class also has an assigned URL. The URL for the 
   collection of blog posts could be /api/posts/ and the URL for the collection of all comments could be /api/comments/.

4. Request methods: GET, POST, PUT, DELETE
POST: Create a new resource and add it to the collection. The server 201 chooses the URL of the new resource and returns it in a Location header in the response.

PUT: Modify an existing resource. Alternatively, this method can also be used to create a new resource when the client can choose the resource URL.

5. REST does not specify the format to use to encode resources 
The Content-Type header in requests and responses is used to indicate the format in which a resource is encoded in the body. The two formats commonly used with RESTful web services are JavaScript Object Notation (JSON) and Extensible Markup Language (XML)

6. Versioning: The situation with RIAs and web services is more complicated than traditional services, because often clients are developed independently of the server—maybe even by different people. Example: client on the web browser can be updated at any time, but app on smartphone
cannot. => For these reasons, web services need to be more tolerant than regular web applica‐ tions and be able to work with old versions of their clients. 
=> web services are given versions: /api/v1/posts/ or /api/v2/posts/

7. Authentication: web services need to protect data of the user hence they ask 
	credetentials of the ser and check them on the server side. But according to REST
	the web services must be 'stateless' => they mustn't remember anything about the user
	that's why they store the data about the user session (client-side cookie). 
	However, 'the use of cookies in RESTful web services falls into a gray area'.

	That's why the best option is to use 'HTTP authentication': With HTTP authentication, user credentials are included in an Authorization header with all requests.
