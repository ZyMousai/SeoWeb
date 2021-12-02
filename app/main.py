# from typing import Optional

from fastapi import FastAPI

from voluum_app.view import volumm_api
from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.background import BackgroundScheduler

from voluum_spider.VoluumSpider import VoluumData

app = FastAPI(title="SeoWeb", version="1.0")

# 注册蓝图
app.include_router(volumm_api, tags=["Volumm_api"])

# 跨域
# allow_origins 允许的url列表
# allow_methods 允许的请求方式
# allow_headers 允许的请求头
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

# ==================分割线==================
# 定时任务
ax = VoluumData()

master_scheduler = BackgroundScheduler(timezone='Pacific/Pitcairn',
                                       job_defaults={'coalesce': True, 'misfire_grace_time': 60 * 60 * 2},
                                       SCHEDULER_API_ENABLED=True)

# 定时刷新库里的campaign信息
master_scheduler.add_job(ax.add_campaign, "interval", seconds=600)

master_scheduler.start()
