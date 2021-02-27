from users.models import CustomUser as User
from django.shortcuts import get_object_or_404
from core.models import MessageModel, File
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from urllib.parse import urlparse


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')
    size = SerializerMethodField()
    

    def create(self, validated_data):
        print(validated_data)
        print(self.context['request'].POST)
        user = self.context['request'].user
        attachment= urlparse(self.context['request'].POST['filepath']).path[1:]
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user,attachment=attachment, attachmentName = self.context['request'].POST['filename'])
        msg.save()
        #,
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body', 'attachment', 'attachmentName', 'size')

    def get_size(self, instance):
        try:
            name='attachment/' + instance.attachmentName
            att = File.objects.get(attachment=name)
            return "File size" + str(att.attachment.size + "bytes")
        except:
            return ''
        
class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
