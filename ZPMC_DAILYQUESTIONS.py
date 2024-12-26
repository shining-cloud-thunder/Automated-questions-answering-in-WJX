import time
import pymysql
from time import sleep
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# 测试git
# 数据库连接选项
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'zpmc_dailyquestions'

# 以下内容一般不可以修改-------------------------------------------------------------------------------------------------------------
# 数据库连接模块
try:
    db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    # 设置数据库游标
    cursor = db.cursor()
    # 创建数据库表（存在会pass）
    try:
        cursor.execute('CREATE TABLE IF NOT EXIST question_right_answer (id INT PRIMARY KEY, right_answer VARCHAR(1000))')
        cursor.execute('CREATE TABLE IF NOT EXIST questions_options (id INT PRIMARY KEY, option_A VARCHAR(1000), option_B VARCHAR(1000), option_C VARCHAR(1000), option_D VARCHAR(1000), option_E VARCHAR(1000), option_F VARCHAR(1000), option_G VARCHAR(1000))')
        cursor.execute('CREATE TABLE IF NOT EXIST questions_title (id INT PRIMARY KEY, title VARCHAR(1000))')
        cursor.execute('CREATE TABLE IF NOT EXIST user_scores (user_work_id VARCHAR(100) , scores VARCHAR(1000))')
        cursor.execute('CREATE TABLE IF NOT EXIST users (user_work_id VARCHAR(100), user_name VARCHAR(100) PRIMARY KEY, user_department VARCHAR(1000))')
        db.commit()
    except pymysql.err.OperationalError as e:
        pass

except pymysql.Error as e:
    print("数据库连接失败" + str(e))

# 详细信息输入
input_name = input("你的名字是?\n")
NAME = input_name
cursor.execute("SELECT user_name FROM users")
name_tuple = cursor.fetchall() # 返回的是一个元组列表
name_list = [tup[0] for tup in name_tuple]
if NAME in name_list:
    try:
        # where=后面一定要加双引号，否则一直报错找不到column！！！！！！！！ 标准模板！！！！！！！
        sql = 'SELECT user_work_id, user_department FROM users WHERE user_name ="%s"' % NAME
        cursor.execute(sql)
        work_number_tuple = cursor.fetchall()
        WORK_NUMBER = work_number_tuple[0][0]
        WORK_DEPARTMENT = work_number_tuple[0][1]
        print("欢迎回来：" + NAME + "\n工号：" +WORK_NUMBER+ "\n部门："+WORK_DEPARTMENT)
    except pymysql.err.OperationalError as e:
        print(e)
else:
    print("数据库没发现你的信息，你是新来的！")
    WORK_NUMBER = input("现在输入你的工号！\n")
    WORK_DEPARTMENT = input("再输入你的部门！\n")
    cursor.execute("INSERT INTO users VALUES (%s, %s, %s)", (WORK_NUMBER, NAME, WORK_DEPARTMENT))
    db.commit()

# 答题次数控制
answer_times = input("刷几次？\n")

# 答题休眠时间控制
sleep_time = input("答题完等几秒交卷？\n")

# 操作主函数
def main(this_time):

    # 动作执行类
    class Actions:

        @staticmethod
        def send_keys_by_id(attribute, content):
            driver.find_element("id", attribute).send_keys(content)
            return

        @staticmethod
        def send_keys_by_class(attribute, content):
            driver.find_element("class", attribute).send_keys(content)
            return

        @staticmethod
        def send_keys_by_xpath(attribute, content):
            driver.find_element("xpath", attribute).send_keys(content)
            return

        @staticmethod
        def click_by_id(attribute):
            driver.find_element("id", attribute).click()
            return

        @staticmethod
        def click_by_class(attribute):
            driver.find_element("class", attribute).click()
            return

        @staticmethod
        def click_by_xpath(attribute):
            driver.find_element("xpath", attribute).click()
            return

        @staticmethod
        def obtain_information_by_id(attribute):
            element = driver.find_element("id", attribute)
            return element.text

        @staticmethod
        def obtain_information_by_xpath(attribute):
            element = driver.find_element("xpath", attribute)
            return element.text

        @staticmethod
        def obtain_attribute_by_xpath(attribute, attribute_name):
            element = driver.find_element("xpath", attribute)
            return element.get_attribute(attribute_name)

    # 选择选项类，纯xpath选定标签
    class Answer:
        def __init__(self, xpath):
            self.xpath = xpath

        def answer_a(self):
            Actions.click_by_xpath(self.xpath + "/div[1]/span/a")
            return

        def answer_b(self):
            Actions.click_by_xpath(self.xpath + "/div[2]/span/a")
            return

        def answer_c(self):
            Actions.click_by_xpath(self.xpath + "/div[3]/span/a")
            return

        def answer_d(self):
            Actions.click_by_xpath(self.xpath + "/div[4]/span/a")
            return

        def answer_e(self):
            Actions.click_by_xpath(self.xpath + "/div[5]/span/a")
            return

        def answer_f(self):
            Actions.click_by_xpath(self.xpath + "/div[6]/span/a")
            return

    URL = 'https://kaoshi.wjx.top/vm/Q07QMNw.aspx'
    # 启动selenium开始自动化测试
    driver = webdriver.Chrome(service=Service(r'F:\chromedriver-win64\chromedriver-win64\chromedriver.exe'))
    # 办公室笔记本驱动地址：D:\Learning\chromedriver-win64\chromedriver.exe
    # 宿舍电脑驱动地址：F:\chromedriver-win64\chromedriver-win64\chromedriver.exe

    # 加载网页
    driver.get(URL)
    # 读取网页，不会导致网页被二次加载
    html_content = driver.page_source

    Actions.send_keys_by_id("q1_0", NAME)
    Actions.send_keys_by_id("q1_1", WORK_NUMBER)

    # 选择“员工、劳务工”选项
    Actions.click_by_xpath("/html/body/div[2]/form/div[11]/div[5]/fieldset/div[2]/div[2]/div[1]/span/a")
    sleep(1)
    # 选择部门，打开部门下拉选框
    Actions.click_by_id("q3")
    # 点击选择部门选框，最多等待2秒
    WebDriverWait(driver, 2).until(EC.presence_of_element_located(("xpath","/html/body/div[4]/div[2]/div/div/div[2]/div[1]/div/span/span[1]/span/span[1]"))).click()
    # 选择答题人的部门,按下多少次
    for i in range(102):
        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
    # 回车选定
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    Actions.click_by_xpath("/html/body/div[4]/div[2]/div/div/div[5]/a")

    # 传输刷题人信息到数据库
    try:
        sql = "INSERT INTO users(user_work_id, user_name, user_department) VALUE (%s, %s, %s)"
        value = (WORK_NUMBER, NAME, WORK_DEPARTMENT)
        cursor.execute(sql, value)
        db.commit()
        print(f"{NAME}的信息已经被传输到数据库！")
    except pymysql.err.IntegrityError as e:
        pass
    # 到此基本信息填写完成---------------------------------------------------------------------------------------------------

    # 查询父标签下有多少子标签,recursive=False表示只查询当前父标签下的子标签，不对子标签在进行搜索
    def count_child_tags(parent_tag):
        return len(parent_tag.find_all(recursive=False))

    QUESTIONS_BLOCK_XPATH = "/html/body/div[2]/form/div[11]/div[5]/fieldset"
    QUESTIONS_BLOCK_LIST_XPATH = []
    QUESTIONS_ANSWER_BLOCK_LIST_XPATH = []

    # 问题的id
    QUESTION_IDS = []

    QUESTION_TITLES = []
    # OPTIONS = []
    for j in range(6, 11):
        # 问题块xpath
        QUESTION_BLOCK_LIST_XPATH = str(QUESTIONS_BLOCK_XPATH + "/div[" + str(j) + "]")
        # 问题题干xpath
        QUESTION_BLOCK_LIST_TITLE_XPATH = str(QUESTIONS_BLOCK_XPATH + "/div[" + str(j) + "]" + "/div[1]/div")
        # 问题选项块xpath
        QUESTION_OPTIONS_BLOCK_XPATH = str(QUESTIONS_BLOCK_XPATH + "/div[" + str(j) + "]" + "/div[2]")

        # 添加到相应的列表
        QUESTIONS_BLOCK_LIST_XPATH.append(QUESTION_BLOCK_LIST_XPATH)
        QUESTIONS_ANSWER_BLOCK_LIST_XPATH.append(str(QUESTIONS_BLOCK_XPATH + "/div[" + str(j) + "]" + "/div[2]"))

        # 问题题干的id
        QUESTION_ID = Actions.obtain_attribute_by_xpath(QUESTION_BLOCK_LIST_XPATH, "topic")
        QUESTION_IDS.append(QUESTION_ID)

        # 问题题干的文本
        QUESTION_TITLE = Actions.obtain_information_by_xpath(QUESTION_BLOCK_LIST_TITLE_XPATH)
        QUESTION_TITLES.append(QUESTION_TITLE)

        # 问题题干传入到所有数据库表格中
        try:
            sql = "INSERT INTO questions_title(id, title) VALUE (%s, %s)"
            value = (QUESTION_ID, QUESTION_TITLE)
            cursor.execute(sql, value)
            db.commit()
        # 存在主键相同错误
        except pymysql.err.IntegrityError as e:
            pass
        # 问题的id传入到选项数据库中
        try:
            sql = "INSERT INTO questions_options(id) VALUE (%s)"
            value = (QUESTION_ID)
            cursor.execute(sql, value)
            db.commit()
        except pymysql.err.IntegrityError as e:
            pass

    QUESTION_OPTIONS = []
    #对选项块内的选项进行解析，数出题目中的选项个数
    soup = BeautifulSoup(html_content, "html.parser")
    # 筛选出所有满足要求的div，这里的parent_tags是所有的题的选项区域的div
    parent_tags = soup.find_all("div", {"class": "ui-controlgroup column1"}, recursive=True)
    # 这里的parent_tag是每一题的选项区域的div
    for parent_tag in parent_tags:
        options = []
        for option in parent_tag:
            options.append(option.text)
        QUESTION_OPTIONS.append(options)

    # 将选项数据传输到数据库中 questions_options id option_A~G
    k = 0
    for questions_options_block in QUESTION_OPTIONS:
        ascii_value = 65 # A
        for option in questions_options_block:
            character = chr(ascii_value)
            try:
                sql = "UPDATE questions_options SET option_" + character + "=%s WHERE id=%s"
                value = (option, QUESTION_IDS[k])
                cursor.execute(sql, value)
                db.commit()
            except pymysql.err.IntegrityError as e:
                pass
            ascii_value += 1
            character = chr(ascii_value)
        k += 1

    # 答题模块
    recognized_number = 0
    cursor.execute("SELECT id FROM question_right_answer")
    ids_tuple = cursor.fetchall()
    ids_list2 = [tup[0] for tup in ids_tuple]
    # 把ids_list内的元素转换成str
    ids_list = [int(content) for content in ids_list2]
    # print(ids_list[0])
    for k in range(len(QUESTIONS_ANSWER_BLOCK_LIST_XPATH)):
        Answer_test = Answer(QUESTIONS_ANSWER_BLOCK_LIST_XPATH[k])
        if int(QUESTION_IDS[k]) not in ids_list:
            #  问题的id传入到正确选项数据库中
            try:
                sql = "INSERT INTO question_right_answer(id) VALUE ("+f"{QUESTION_IDS[k]}"+")"
                # value = (QUESTION_ID[k])
                cursor.execute(sql)
                db.commit()
            except pymysql.err.IntegrityError as e:
                pass
            # 没见过的题目全部选第一个选项
            Answer_test.answer_a()
        else:
            recognized_number += 1
            result = cursor.execute("SELECT right_answer FROM question_right_answer WHERE id="+f"{int(QUESTION_IDS[k])}")
            answer_tuple = cursor.fetchall()
            answer_list = [tup[0] for tup in answer_tuple]
            for row in answer_list:
                if "对" in row:
                    Answer_test.answer_a()
                if "错" in row:
                    Answer_test.answer_b()
                if "A" in row:
                    Answer_test.answer_a()
                if "B" in row:
                    Answer_test.answer_b()
                if "C" in row:
                    Answer_test.answer_c()
                if "D" in row:
                    Answer_test.answer_d()
                if "E" in row:
                    Answer_test.answer_e()
                if "F" in row:
                    Answer_test.answer_f()

    # 答题完成后的休眠时间
    time.sleep(int(sleep_time))
    # 确认答题
    Actions.click_by_id("ctlNext")
    # 到此答题完成--------------------------------------------------------------------------------------------------------------

    # 打开答题解析，最多等待3秒跳转
    WebDriverWait(driver, 3).until(EC.presence_of_element_located(("xpath","/html/body/div[2]/div[2]/div[1]/div[2]/div/div[2]/a/span"))).click()

    # 获取答题分数
    score = Actions.obtain_information_by_xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div")
    print(f"第{this_time + 1}次拿到了{score}分，识别到{recognized_number}题答案")
    if int(recognized_number)*20 > int(score):
        print(QUESTION_IDS)
        input('题库识别与分数对应不了，答案出现问题')

    # 将分数放在数据库中
    try:
        sql = "INSERT INTO user_scores(user_work_id, scores) VALUE (%s, %s)"
        value = (WORK_NUMBER, score)
        cursor.execute(sql, value)
        db.commit()
    except pymysql.err.IntegrityError as e:
        pass

    # 开始解析答案，并放入数据库
    ANSWER_BLOCK_XPATH = "/html/body/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div"
    ANSWER_BLOCK_LIST_XPATH = []
    for i in range(4, 9):
        blocks = str(ANSWER_BLOCK_XPATH + "/div[" + str(i) + "]")
        ANSWER_BLOCK_LIST_XPATH.append(blocks)
        if Actions.obtain_information_by_xpath(blocks + "/div[2]/div/div[2]/span") == "回答正确":
            try:
                sql = "UPDATE question_right_answer SET right_answer=%s WHERE id=%s"
                value = ("A", QUESTION_IDS[i-4])
                cursor.execute(sql, value)
                db.commit()
            except pymysql.err.IntegrityError as e:
                print(e)
        else:
            corret_answer = Actions.obtain_information_by_xpath(blocks + "/div[2]/div/div[3]/div")
            corret_answer_list = []
            for corret_answer in corret_answer.split('┋'):
                corret_answer_list.append(corret_answer[0])
            # 答案选项合并
            combined_string = ''.join(corret_answer_list)
            try:
                sql = "UPDATE question_right_answer SET right_answer=%s WHERE id=%s"
                value = (combined_string, QUESTION_IDS[i-4])
                cursor.execute(sql, value)
                db.commit()
            except pymysql.err.IntegrityError as e:
                print(e)
    driver.quit()
for this_time in range(int(answer_times)):
    main(this_time)

db.close()