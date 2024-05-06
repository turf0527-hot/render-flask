# -*- coding: utf-8 -*-#
import json,requests,time,random
from abc import ABC, abstractmethod


class JslpaCourses():
    def __init__(self):
        self.gl_flag = True
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "http://www.jslpa.cn",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.cookies = {
            "xn_dvid_kf_20023": "E9BCBE-F2F3CE99-17A7-1EA8-B3E9-08A6CBC85A18",
            "p_h5_u": "613B487A-98E8-4B2B-998B-6C04AC4987EB",
            "xn_sid_kf_20023": "1714954135532125",
            "SECKEY_ABVK": "MlSLrpCwVzgwYsaNNYnBd6iTzPzCTK/OpwyLLnYK2wM%3D",
            "ASP.NET_SessionId": "ddkeqtb3zdsh0dxoj44vofe3",
            "BMAP_SECKEY": "MlSLrpCwVzgwYsaNNYnBd41Yg2exYhKUUtkh4Nz-DWFjHZu5zuuZtOHlwiXYy3DECfpMU-PuUSdPQZ31qw1K7bEu6ZPxSHK9p0nHoFRWrGIywRn9M8LfERwRg6xmcazXbkrgGIF9MIrck5J-iWd-ZUY9eiOaY8VKm2SMFmkuR8AcKoDYVKQPYYUtL_yPcSzq"
        }

    def save_cur_time(self,course):
        class_id = course.get("ClassID")
        class_name = course.get("ClassSetName")
        class_url = "http://www.jslpa.cn/api/Course/Details"
        ref = f"http://www.jslpa.cn/CourseDetail/{class_id}"
        class_data = {"classid": class_id}
        self.headers["Referer"] = ref
        # 获取当前课程下有多少章节内容
        class_data = json.dumps(class_data, separators=(',', ':'))
        response = requests.post(class_url, headers=self.headers, cookies=self.cookies, data=class_data)
        if response:
            # print(response.json())
            res = response.json().get("res")
            chapter_list = res.get("chapters")
            for index, chapter in enumerate(chapter_list):
                chapter_id = chapter.get("KEYLIST")
                duration = chapter.get("duration")
                degree = chapter.get("DEGREE")

                if degree == 0:  # 未完成学习
                    print(f"⏩ {class_name} 第{index + 1}章 开始学习")
                    # 获取当前章节学习情况
                    chapter_url = "http://www.jslpa.cn/api/Course/Play"
                    data = {"ChapterID": chapter_id}
                    data_ds = json.dumps(data, separators=(',', ':'))
                    response = requests.post(chapter_url, headers=self.headers, cookies=self.cookies, data=data_ds)
                    if response:
                        # print(response.json())
                        res = response.json().get("res")
                        cur_time = res.get("times")
                        self.learning_course(data, cur_time, duration)
                else:
                    print(f"✅ {class_name} 第{index + 1}章 已完成")
                # 验证是否能答题
                last_url = "http://www.jslpa.cn/api/Course/Chapter"
                data = {"ChapterID": chapter_id, "ClassID": class_id}
                data_ds = json.dumps(data, separators=(',', ':'))
                response = requests.post(last_url, headers=self.headers, cookies=self.cookies, data=data_ds)
                if response:
                    print(response.json())


    def learning_course(self, data, cur_time, duration):
        if (cur_time + 60) >= duration:
            cur_time = duration
        else:
            cur_time += 60
        # wait_time = random.randrange(5, 15, 2)
        wait_time = 60
        sleep_str = "⏩ 停顿 %s 秒;" % wait_time
        p_s = cur_time / duration * 100
        video_str = "视频进度: %.2f" % p_s
        print(sleep_str, video_str, "%")
        time.sleep(wait_time)
        learning_url = "http://www.jslpa.cn/api/Course/Times"
        data["times"] = cur_time
        data_ds = json.dumps(data, separators=(',', ':'))
        response = requests.post(learning_url, headers=self.headers, cookies=self.cookies, data=data_ds)
        print(response.text)
        if cur_time != duration:
            self.learning_course(data, cur_time, duration)

    def get_course_list(self):
        course_list = []
        url = "http://www.jslpa.cn/api/Course/List"
        self.headers["Referer"] = "http://www.jslpa.cn/UserView/CourseList"
        response = requests.post(url, headers=self.headers, cookies=self.cookies, verify=False)
        if response:
            res = response.json()
            print(res.get("msg"))
            res_list = res.get("res")
            zy_list = res_list[0].get("list")
            gx_list = res_list[0].get("gxk_list")
            return zy_list, gx_list

    def get_flag(self):
        return self.gl_flag

    def change_flag(self):
        self.gl_flag = not self.gl_flag

    def jslpa_main(self):
        print("🌈 江苏省执业药师继续教育学习中...")
        zy_list, gx_list = self.get_course_list()
        # print(zy_list)
        # zy_list.extend(gx_list)
        for course in zy_list:
            self.save_cur_time(course)
        self.gl_flag = False
