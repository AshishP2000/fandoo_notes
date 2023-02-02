from rest_framework import serializers

from note.models import Notes, Labels


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'note_title', 'note_body', 'user']


class CollaboratorSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.collaborator.add(*validated_data.get('collaborator'))
        instance.save()
        return instance

    class Meta:
        model = Notes
        fields = ['id', 'collaborator']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['id', 'title', 'color', 'user']
        ref_name = 'LabelSerializer'


class LabelNoteSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.label.add(*validated_data.get('label'))
        instance.save()
        return instance

    class Meta:
        model = Notes
        fields = ['id', 'label']
