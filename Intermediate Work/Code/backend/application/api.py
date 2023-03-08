from flask_restful import Resource, request, abort
from flask import jsonify
from datetime import datetime
from dateutil import tz, parser
from application.models import User, Student, Admin, Manager, Response, Ticket, FAQ, Category
from application.models import token_required, db

class TicketAPI(Resource):
    @token_required
    def get(user,self):
        if(user.role_id==1):
            ticket=Ticket.query.filter_by(creator_id=user.user_id).all()
            result=[]
            for t in ticket:
                d={}
                d['ticket_id']=t.ticket_id
                d['title']=t.title
                d['description']=t.description
                d['creation_date']=str(t.creation_date)
                d['creator_id']=t.creator_id
                d['number_of_upvotes']=t.number_of_upvotes
                d['is_read']=t.is_read
                d['is_open']=t.is_open
                d['is_offensive']=t.is_offensive
                d['is_FAQ']=t.is_FAQ
                result.append(d)
            return jsonify(result)
        else:
            abort(403,message="You are not authorized to view this page")
    @token_required
    def post(user,self):
        if(user.role_id==1):
            data=request.get_json()
            ticket=Ticket(title=data['title'],
                          description=data['description'],
                          creation_date=datetime.now(),
                          creator_id=user.user_id,
                          number_of_upvotes=data['number_of_upvotes'],
                          is_read=data['is_read'],
                          is_open=data['is_open'],
                          is_offensive=data['is_offensive'],
                          is_FAQ=data['is_FAQ'])
            db.session.add(ticket)
            db.session.commit()
            return jsonify({'message':'Ticket created successfully'})
        else:
            abort(403,message="You are not authorized to view this page")
        
    @token_required
    def patch(user, self):
        if user.role_id==1:
            args = request.get_json(force = True)
            a = None
            try:
                a = int(args["ticket_id"])
                #print(a)
                #print(user.user_id)
            except:
                abort(403, message = "Please mention the ticketId field in your form")
            ticket = None
            try:
                ticket = Ticket.query.filter_by(ticket_id = a, creator_id = user.user_id).first()
            except:
                abort(404, message = "There is no such ticket by that ID")
            title = None
            try:
                title = args["title"]
                ticket.title = title
            except:
                pass
            description = None
            try:
                description = args["description"]
                ticket.description = description
            except:
                pass
            number_of_upvotes = None

            try:
                number_of_upvotes = int(args["number_of_upvotes"])
                ticket.number_of_upvotes = number_of_upvotes
            except:
                pass
            is_read = None
            try:
                if args["is_read"] is not None:
                    is_read = args["is_read"]
                    ticket.is_read = is_read
            except:
                pass
            is_open = None
            try:
                if args["is_open"] is not None:
                    is_open = args["is_open"]
                    ticket.is_open = is_open
            except:
                pass
            is_offensive = None
            try:
                if args["is_offensive"] is not None:
                    is_offensive = args["is_offensive"]
                    ticket.is_offensive = is_offensive
            except:
                pass
            is_FAQ = None
            try:
                if args["is_FAQ"] is not None:
                    is_FAQ = args["is_FAQ"]
                    ticket.is_FAQ = is_FAQ
            except:
                pass   
            db.session.commit()
            return jsonify({"message": "success"})
        
        else:
            abort(403,message= "You are not authorized to access this!")
        
    @token_required
    def delete(user, self):
        try:
            ticket_id = int(request.get_json()['ticket_id'])
        except:
            abort(400, 'ticket_id must exist and should be integer')
        current_ticket = db.session.query(Ticket).filter(Ticket.ticket_id==ticket_id,Ticket.creator_id==user.user_id).first()
        if current_ticket:
            responses = db.session.query(Response).filter(Response.ticket_id==ticket_id).all()
            if responses:
                for post in responses:
                    db.session.delete(post)
                    db.session.commit() 
            db.session.delete(current_ticket)
            db.session.commit()
            return 200, "OK"
        else:
            abort(400, message='No such ticket_id exists for the user')

import secrets,string    
from random_username.generate import generate_username   

class UserAPI(Resource):
    @token_required
    def get(user,self):
        if(user.role_id==3):
            user=User.query.all()
            result=[]
            for user in user:
                if(user.role_id==1 or user.role_id==2):
                    d={}
                    d['user_id']=user.user_id
                    d['user_name']=user.user_name
                    d['email_id']=user.email_id
                    d['role_id']=user.role_id
                    result.append(d)
            return jsonify(result)
        else:
            abort(403,message="You are not authorized to view this page")
    @token_required
    def post(user,self):
        if(user.role_id==3):
            data=request.get_json()
            secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
            user_name=generate_username(1)[0]
            user=User(user_name=user_name,email_id=data['email_id'],password=secure_str,role_id=data['role_id'])
            db.session.add(user)
            db.session.commit()
            return jsonify({'message':'User created successfully'})
        else:
            abort(403,message="You are not authorized to view this page")
    @token_required
    def delete(user, self):
        try:
            user_id = int(request.get_json()['user_id'])
        except:
            abort(400, 'user_id must exist and should be integer')
        current_user = User.query.filter(User.user_id==user_id).first()
        if current_user:
            db.session.delete(current_user)
            db.session.commit()
            return 200, "OK"
        else:
            abort(400, 'No such user_id exists')
    @token_required
    def patch(user,self):
        args=request.get_json(force=True)
        user_id=None
        current_user=None
        try:
            user_id=int(args['user_id'])
        except:
            abort(400,message="user_id must exist and should be integer")
        try:
            current_user=User.query.filter(User.user_id==user_id).first()
        except:
            abort(400,message="No such user_id exists")
        user_name=None
        try:
            user_name=args['user_name']
            current_user.user_name=user_name
        except:
            pass
        try:
            password=args['password']
            current_user.password=password
        except:
            pass
        try:
            email_id=args['email_id']
            if(user.role_id==3):
                current_user.email_id=email_id
            else:
                abort(403,message="You are can't edit email")
        except:
            pass
        db.session.commit()
        return jsonify({'message':'User updated successfully'})
    

class FAQApi(Resource):
    @token_required
    def get(user,self):
        if user.role_id==3:
            faq = db.session.query(FAQ).all()
            result = []
            for q in faq:
                d = {}
                d['ticket_id'] = q.ticket_id
                d['category'] = q.category
                d['is_approved'] = q.is_approved
                result.append(d)
            return jsonify(result)
            # for q in faq:
            #     d = {}
            #     d['ticket_id'] = q.ticket_id
            #     d['category'] = q.category
            #     d['is_approved'] = q.is_approved
            #     d['title'] = q.ticket.title
            #     d['description'] = q.ticket.description
            #     d['creation_date'] = q.ticket.creation_date
            #     d['creator_id'] = q.ticket.creator_id
            #     d['number_of_upvotes'] = q.ticket.number_of_upvotes
            #     d['is_read'] = q.ticket.is_read
            #     d['is_open'] = q.ticket.is_open
            #     d['is_offensive'] = q.ticket.is_offensive
            #     d['is_FAQ'] = q.ticket.is_FAQ
            #     d['responses'] = []
            #     responses = q.ticket.responses
            #     if responses:
            #         for response in responses:
            #             d2 = {}
            #             d2['response_id'] = response.response_id
            #             d2['responder_id'] = response.responder_id
            #             d2['response_timestamp'] = response.response_timestamp
            #             d2['response'] = response.response
            #             d['responses'].append(d2)
            #     result.append(d)
            # return jsonify(result)
        else:
            abort(403, 'Unauthorized')

    @token_required
    def post(user, self):
        if user.role_id == 3:
            data = request.get_json()
            try:
                tid = int(data['ticket_id'])
            except:
                abort(400, message="ticket_id is required and should be integer")
            try:
                cat = data['category']
            except:
                abort(400, message="category is required and should be string")
            try:
                is_app = data['is_approved']
            except:
                abort(400, message="is_approved is required and should be boolean")

            if not db.session.query(Ticket).filter(Ticket.ticket_id==tid).first():
                abort(400, message="ticket_id does not exist")

            if db.session.query(Category).filter(Category.category==cat).first() is None:
                abort(400, message="category does not exist")

            if not isinstance(is_app, bool):
                abort(400, message="is_approved must be boolean")

            newFAQ = FAQ(ticket_id = tid, category=cat, is_approved=is_app)
            db.session.add(newFAQ)
            db.session.commit()  

            return jsonify({'message': "FAQ added successfully"})               

        else:
            abort(403, message="Unauthorized")
    
    @token_required
    def patch(user, self):
        if user.role_id==3:
            data = request.get_json()
            try:
                tid = int(data['ticket_id'])
            except:
                abort(400, message="ticket_id is required and should be integer")
            try:
                cat = data['category']
            except:
                abort(400, message="category is required and should be string")
            try:
                is_app = data['is_approved']
            except:
                abort(400, message="is_approved is required and should be boolean")

            if not db.session.query(Ticket).filter(Ticket.ticket_id==tid).first():
                abort(400, message="ticket_id does not exist")

            if db.session.query(Category).filter(Category.category==cat).first() is None:
                abort(400, message="category does not exist")

            if not isinstance(is_app, bool):
                abort(400, message="is_approved must be boolean")
            
            current_ticket=db.session.query(FAQ).filter(FAQ.ticket_id==tid).first()
            if current_ticket:
                current_ticket.category = cat
                current_ticket.is_approved = is_app
                db.session.commit()
                return jsonify({'message': "FAQ updated successfully"})
            else:
                abort(400, message="ticket_id is not in FAQ")
        else:
            abort(403, message="Unauthorized")