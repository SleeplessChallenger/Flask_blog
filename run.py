from blog import create_app

app = create_app()
# app.app_context().push()
# if we want another configuration
# then we can provide it here.
# Otherwise, we have default parameter

if __name__ == '__main__':
	app.run(debug=True)
