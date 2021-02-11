from flask import Response, request
from flask_restful import Resource
from mongoengine import DoesNotExist, Q
import models
import json

class CommentListEndpoint(Resource):
    
    def queryset_to_serialized_list(self, queryset):
        serialized_list = [
            item.to_dict() for item in queryset
        ]
        return serialized_list

    def getData(self):
        post_id = request.args.get('post_id')
        if post_id:
            # find data where *any of the fields contain the term...
            data = models.Comment.objects.filter(
                post = post_id 
            )
        else:
            data = models.Comment.objects
        return data

    def get(self): # called when /api/comments 
        # TODO: implement GET endpoint
        data = self.getData()
        # formatting the output JSON
        data = self.queryset_to_serialized_list(data)
        return Response(json.dumps(data), mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        comment = models.Comment(**body).save()
        serialized_data = {
            'id': str(comment.id),
            'message': 'Comment {0} successfully created.'.format(comment.id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=201)


class CommentDetailEndpoint(Resource):
    def put(self, id):
        # TODO: implement PUT endpoint
        comment = models.Comment.objects.get(id=id)
        request_data = request.get_json()
        comment.comment = request_data.get('comment')
        comment.save()
        print(comment.to_json())
        return Response(comment.to_json(), mimetype="application/json", status=200)
    
    def delete(self, id):
        comment = models.Comment.objects.get(id=id)
        comment.delete()
        serialized_data = {
            'message': 'Comment {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

    def get(self, id):
        comment = models.Comment.objects.get(id=id)
        return Response(comment.to_json(), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(CommentListEndpoint, '/api/comments', '/api/comments/')
    api.add_resource(CommentDetailEndpoint, '/api/comments/<id>', '/api/comments/<id>/')
    # api.add_resource(CommentListEndpoint, '/api/posts/<post_id>/comments', '/api/posts/<post_id>/comments/')
    # api.add_resource(CommentDetailEndpoint, '/api/posts/<post_id>/comments/<id>', '/api/posts/<post_id>/comments/<id>/')