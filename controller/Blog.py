import boto3
from controller.Common import Common

dynamo_client = boto3.resource('dynamodb')
blogTable = dynamo_client.Table('Blog')


class Blog:

    def getBlog():
        return dynamo_client.scan(
            TableName='Blog'
        )

    def getBlogById():
        return Common.generateUUID()

    def createBlog(title, blogCategoryId, bodyText, isPublic, isSubscriptionOnly, createdById):
        print(postdata)
    #     blogTable.put_item(
    #    Item={
    #         'ID': Common.generateUUID(),
    #         'BlogCategoryId': blogCategoryId,
    #         'Title': title,
    #         'BodyText': bodyText,
    #         'IsPublic': isPublic,
    #         'IsSubscriptionOnly': isSubscriptionOnly,
    #         'CreatedById': createdById,
    #         'CreatedDate': Common.getDateTimeNow(),
    #         'ModifiedDate': "",
    #         'DeletedDate': ""
    #     }
    # )
        return "New blog is created" + postdata
