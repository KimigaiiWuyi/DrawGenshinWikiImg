import json
import asyncio
from typing import Literal
from httpx import AsyncClient, HTTPError

AMBR = {
    '角色列表': 'https://api.ambr.top/v2/chs/avatar',
    '武器列表': 'https://api.ambr.top/v2/chs/weapon'
}


async def query_ambr(
    type: Literal['角色列表', '武器列表'], retry: int = 3
) -> dict:
    '''安柏计划数据接口请求'''

    async with AsyncClient() as client:
        while retry:
            try:
                res = await client.get(AMBR[type], timeout=10.0)
                return res.json()['data']
            except (HTTPError or json.decoder.JSONDecodeError or KeyError):
                print(f'安柏计划 {type} 接口请求出错，正在重试...')
                retry -= 1
                if retry:
                    await asyncio.sleep(2)
    return {}


async def main():
    weapon_res = await query_ambr('武器列表')
    weapon_dict =weapon_res['items']
    weapon_list=[]

    for values in weapon_dict.values():
        if values['name'] != '':
            weapon_list.append(values['name'])
    print(weapon_list)


asyncio.run(main())
