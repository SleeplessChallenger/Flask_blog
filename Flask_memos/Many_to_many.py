
# 1 association table is required
# where 2 columns between 2 tables will be

# 2 it's better to create standalone table
# rather than class when no custom data required

# 3 db.Table(name of the table, number of columns* desired)
# * name, type, FK

# 4 adding 'attribute' in User to create connection
# first: another table; second: association table;
# third: backref (add so-called column in the Channel class)

# 5 having added data to User & Channel, we can subsribe user
# to the channel: channel1.sub_num.append(user1); db.session.commit()

# 6 then we can see how many/what names are pertinent to the channel:
# for x in channel1.sub_num:
#	print x.name

subs = db.Table('subs', 
	   db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
	   db.Column('post_id', db.Integer, db.ForeignKey('channels.channel_id')))

class User(db.Model):

	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	subsriptions = db.relationship('channels', secondary=subs,
									backref=db.backref('sub_num', lazy='dynamic'),
									lazy='dynamic')



class Channel(db.Model):

	__tablename__ = 'channels'
	channel_id = db.Column(db.Integer, primary_key=True)
	channel_name = db.Column(db.String(20))




# another example
registrations = db.Table('registrations',
				db.Column('student_id', db.Integer, db.ForeignKey('students.id')), 
				db.Column('class_id', db.Integer, db.ForeignKey('classes.id')))


class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	classes = db.relationship('Class', secondary=registrations, 
								backref=db.backref('students', lazy='dynamic'), lazy='dynamic')


class Class(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)

# But to be able to work with custom data in the relationship the association
# table must be upgraded to 'model'.

class Follow(db.Model):

	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
							primary_key=True)

	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
							primary_key=True)

	timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Next, to use aforewritten association table we need to decompose many-to-many into
# 2 one-to-many as 'db.relationship'

class User(UserMixin, db.Model): 
	# ...
	followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
								backref=db.backref('follower', lazy='joined'),
								lazy='dynamic', cascade='all, delete-orphan')

	followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
								 backref=db.backref('followed', lazy='joined'),
								 lazy='dynamic', cascade='all, delete-orphan')
