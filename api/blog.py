from flask import jsonify
from controller.Blog import Blog
from model.apiResponse import ApiResponse


class BlogApi:
    def getAllBlog():
        return jsonify(Blog.getBlog())

    def getBlogById():
        return jsonify(Blog.getBlogById())

    def createBlog():
        return jsonify(Blog.createBlog(title, blogCategoryId, bodyText, isPublic, isSubscriptionOnly, createdById))
