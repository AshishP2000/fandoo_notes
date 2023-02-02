import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from note.models import Notes, Labels
from note.redis_note import RedisNote
from note.serializers import NoteSerializer, CollaboratorSerializer, LabelNoteSerializer, LabelSerializer
from user.utils import verify_user
logging.basicConfig(filename='fundoo_notes.log', level=logging.INFO)


class Note(APIView):

    @verify_user
    def post(self, request):
        """
        This method create note for user
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().save(serializer.data, request.data.get('user'))
            return Response({"message": "Note Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def get(self, request):
        """
        This method retrieves notes of a user
        """
        try:
            notes = Notes.objects.all()
            serializer = NoteSerializer(notes, many=True)
            redis_data = RedisNote().get(request.data.get('user'))
            if len(serializer.data) != 0:
                return Response({"message": "Data Retrieved", "status": 200, "data": redis_data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "No Data", "status": 200},
                                status=status.HTTP_200_OK)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def put(self, request):
        """
        This method update the note of a user
        """
        try:
            note_object = Notes.objects.get(id=request.data.get('id'), user=request.data.get('user'))
            serializer = NoteSerializer(note_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().update(serializer.data, request.data.get('user'))
            return Response({"message": "Note Updated", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def delete(self, request):
        """
        This method delete the note of a user
        """
        try:
            note_object = Notes.objects.get(id=request.data.get('id'), user=request.data.get('user'))
            note_object.delete()
            RedisNote().delete(request.data.get('user'), request.data.get('id'))
            return Response({"message": "Note Deleted", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class NoteCollaborator(APIView):

    @verify_user
    def post(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            serializer = CollaboratorSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Collaborator Added", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            note.collaborator.remove(*request.data.get('collaborator'))
            return Response({"message": "Collaborator Removed", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class Label(APIView):
    """
    This class performs CRUD for Labels model
    """

    @verify_user
    def post(self, request):
        """
        This method create label for notes
        """
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def get(self, request):
        """
        This method get labels from the database
        """
        try:
            label = Labels.objects.filter(user_id=request.data.get('user'))
            serializer = LabelSerializer(label, many=True)
            return Response({"message": "Data Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def put(self, request):
        """
        This method update the labels in the database
        """
        try:
            label = Labels.objects.get(id=request.data.get('id'))
            serializer = LabelSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Updated", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def delete(self, request):
        """
        This method update the labels in the database
        """
        try:
            label = Labels.objects.get(id=request.data.get('id'))
            label.delete()
            return Response({"message": "Label Deleted", "status": 204, "data": {}}, status=status.HTTP_204_NO_CONTENT)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class AddLabelToNote(APIView):

    @verify_user
    def post(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            serializer = LabelNoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Created Label and Note Relationship", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get('id'))
            note.label.remove(*request.data.get('label'))
            return Response({"message": "Label Removed", "status": 204, "data": {}}, status=status.HTTP_204_NO_CONTENT)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
