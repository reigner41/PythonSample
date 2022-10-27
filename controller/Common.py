class Common:    

    def generateUUID():
        import uuid
        # make a UUID based on the host ID and current time
        uuid = uuid.uuid1()
        uuid1 = str(uuid)
        uuid2 = uuid1.replace('-', '')
        return uuid2

    def getDateTimeNow():
        mdt = timezone('Greenwich')
        now = datetime.now(mdt)
        dateTimeNow = now.strftime("%Y-%m-%d %H:%M:%S")
        return dateTimeNow

    def strToDate(self, strDate):
        #code goes here
        return "date to string"