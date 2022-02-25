from alarm_guide import manager
from database_manager import Manager
from alarm_guide.alarms import Alarm
from alarm_guide.parts import Part


class Post:
    def __init__(self, post_id, f_name, l_name, created, content):
        self.post_id = post_id
        self.f_name = f_name
        self.l_name = l_name
        self.created = created
        self.content = content
        self.image_files = []

    def fill_image_files(self, manager: Manager):
        image_files = manager.get(f"SELECT * FROM entries_images WHERE identries = {self.post_id}")
        if image_files:
            self.image_files = image_files


class Posts:
    def __init__(self, manager: Manager):
        self.manager = manager
        self.vendor: int
        self.model: int
        self.module: int
        self.alarm_id: str
        self.idalarm = ''
        self.alarm_card = ''
        self.posts = []
        self.parts = []

    def process_form(self, form):
        self.vendor = form.vendor.data
        self.model = form.model.data
        self.module = form.module.data
        self.alarm_id = form.alarm_id.data

    def process_dict(self, data):
        self.vendor = data['vendor']
        self.model = data['model']
        self.module = data['module']
        self.alarm_id = data['alarm_id']

    def process_request(self, request):
        self.vendor = request.form.get('vendor')
        self.model = request.form.get('model')
        self.module = request.form.get('module')
        self.alarm_id = request.form.get('alarm_id')

    def get_alarm(self):
        alarm = self.manager.get(
            f"SELECT * FROM alarms WHERE eqp_module = {self.module} AND alarm_id = '{self.alarm_id}' ")
        if alarm:
            self.alarm_card = Alarm(alarm[0][2], alarm[0][3], alarm[0][4], alarm[0][5], alarm[0][6])
            self.idalarm = int(alarm[0][0])

    def get_posts(self):
        if self.idalarm:
            posts = self.manager.get(f"""
                                SELECT identries, f_name, l_name, date, entry FROM entries
                                INNER JOIN tech
                                ON entries.user_id = tech.idtech
                                WHERE entries.idalarm = {self.idalarm};
                                """)
            for post in posts:
                self.posts.append(Post(post[0], post[1], post[2], post[3], post[4]))

    def get_parts(self):
        if self.idalarm:
            parts = self.manager.get(f"""
                                SELECT q_number, vendor_pn, description FROM alarm_parts_common
                                INNER JOIN ordered_parts
                                ON alarm_parts_common.idordered_parts = ordered_parts.idordered_parts
                                WHERE alarm_parts_common.idalarms = {self.idalarm};""")
            for part in parts:
                self.parts.append(Part(part[0], part[1], part[2]))

    def fill(self):
        self.get_alarm()
        if self.idalarm:
            self.get_posts()
            self.get_parts()


class AddPost:

    def __init__(self, manager: Manager):
        self.manager = manager
        self.user_id: int
        self.idalarm: int
        self.entry: str

    def processRequest(self, request):
        self.user_id = request.form.get('user_id')
        self.idalarm = request.form.get('idalarm')
        self.entry = request.form.get('entry')

    def post(self):
        sql = "INSERT INTO entries(user_id, idalarm, entry) VALUES(%s, %s, %s)"
        values = (int(self.user_id), int(self.idalarm), self.entry)
        self.manager.post(sql, values)

    def __repr__(self):
        return f"AddPost(user_id={self.user_id}, idalarm={self.idalarm}, entry='{self.entry}')"

