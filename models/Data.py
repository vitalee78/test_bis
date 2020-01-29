class DateApp:
    def __init__(self, id_goods=None, order_name=None, order_email=None, order_phone=None, order_comment=None,
                 commit_window=None):
        self.id_goods = id_goods
        self.order_name = order_name
        self.order_email = order_email
        self.order_phone = order_phone
        self.order_comment = order_comment
        self.commit_window = commit_window

    def __repr__(self):
        return f'{self.id_goods} {self.order_name} {self.order_phone} {self.order_email} {self.order_comment} {self.commit_window}'
