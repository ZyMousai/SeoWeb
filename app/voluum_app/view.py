import random
from fastapi import APIRouter, Request, Depends

from public_p.mongo_c.MongoClient import MongoClient
from sql_models.voluum_app_model.voluum_model import DBCampaignMapping, CampaignMapping
from voluum_spider.VoluumSpider import VoluumSpider

volumm_api = APIRouter(
    prefix="/volumm_api/v1.0",
    responses={404: {"description": "Not found"}},
)


def db(request: Request):
    return request.state.db


@volumm_api.get('/campaign')
async def get_campaign(request: Request):
    """查询所有的campaign信息"""
    response_body = {
        'ret_code': 200,
        'ret_msg': f'{request.url} Success',
        'ret_data': {}
    }
    mongo = MongoClient()
    query_body = mongo.select('voluum_campaigns')

    response_body['ret_data'] = query_body
    return response_body


@volumm_api.get('/supplement/{campaign_id}')
async def get_campaign_supplement(campaign_id: str, request: Request):
    """查询一个campaign需要的补量"""
    response_body = {
        'ret_code': 200,
        'ret_msg': f'{request.url} Success',
        'ret_data': {}
    }
    return response_body


@volumm_api.get('/campaign_site_url/{campaign_id}')
async def get_campaign_site_url(campaign_id: str, request: Request, db=Depends(db)):
    """生成携带site-id的campaign_url"""
    response_body = {
        'ret_code': 200,
        'ret_msg': f'{request.url} Success',
        'ret_data': {}
    }

    # 1. 拿到数据 可以获取到此campaign_id最近的site-id
    ax = VoluumSpider()
    ax.get_token()
    body = ax.get_one_reports(campaign_id)['body']

    # 2. 根据 uniqueClicks 进行排序获取 site-id
    c_c = {i['customVariable2']: i['uniqueClicks'] for i in body}
    c_c_sort = {k: v for k, v in sorted(c_c.items(), key=lambda item: item[1], reverse=True)}

    site_id_list = []

    for x, v in c_c_sort.items():
        if int(v) == 0:
            continue
        elif x.isdigit():
            site_id_list.append(x)
        else:
            pass
    site_id = random.choice(site_id_list[4:10])

    # 3. 根据campaigns-id获取url
    # 通过主id拿到从id，查询主id最近的site，但是更换的链接是从id
    cam_m_s_mapping = await DBCampaignMapping.get_one(db, campaign_id)
    mongo = MongoClient()
    # query_ = mongo.select('voluum_campaigns', **{'id': campaign_id})[0]
    query_ = mongo.select('voluum_campaigns', **{'id': cam_m_s_mapping.s_id})[0]
    url = query_['impressionUrl'].replace('{site_id}', site_id)
    if '/impression' in url:
        url = url.replace('/impression', '')
    response_body['ret_data'] = url

    return response_body


@volumm_api.get('/campaign_mapping')
async def get_campaign_mapping(request: Request, db=Depends(db)):
    response_body = {'ret_code': 200, 'ret_msg': f'{request.url} Success',
                     'ret_data': await DBCampaignMapping.get_all(db)}
    return response_body


@volumm_api.post('/campaign_mapping')
async def add_campaign_mapping(request: Request, user: CampaignMapping, db=Depends(db)):
    response_body = {'ret_code': 200, 'ret_msg': f'{request.url} Success',
                     'ret_data': await DBCampaignMapping.add(db, user)}
    return response_body


@volumm_api.delete("/campaign_mapping")
async def delete_campaign_mapping(request: Request, userId: int, db=Depends(db)):
    response_body = {'ret_code': 200, 'ret_msg': f'{request.url} Success',
                     'ret_data': await DBCampaignMapping.delete(db, userId)}
    return response_body
