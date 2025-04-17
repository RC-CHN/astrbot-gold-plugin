from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("goldprice", "RC-CHN", "招商银行黄金行情查询插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 gold。注册成功后，发送 `/gold` 就会触发这个指令
    @filter.command("gold")
    async def gold(self, event: AstrMessageEvent):
        """查询招商银行黄金实时行情"""
        import aiohttp
        
        try:
            import os
            url = "https://m.cmbchina.com/api/rate/gold"
            timeout = aiohttp.ClientTimeout(total=10)
            proxy = os.environ.get('http_proxy') or os.environ.get('HTTP_PROXY')
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, proxy=proxy) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    result = "=== 招商银行黄金行情 ===\n"
                    result += f"更新时间: {data['body']['time']}\n\n"
                    
                    for item in data['body']['data']:
                        if item['curPrice'] != '0':
                            result += f"品种: {item['variety']}\n"
                            result += f"当前价: {item['curPrice']}\n"
                            result += f"涨跌幅: {item['upDown']}\n"
                            result += f"最高价: {item['high']}\n"
                            result += f"最低价: {item['low']}\n\n"
                    
                    yield event.plain_result(result)
                    
        except Exception as e:
            yield event.plain_result(f"查询黄金行情失败: {str(e)}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
