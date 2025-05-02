import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

BASE_URL = "https://neko.0g0.jp"

mcp = FastMCP("NEKOESA MCP Server")


class NekoesaDataInfo(BaseModel):
    average: int = Field(description="指定した期間の日毎の平均給餌量")
    cant: int = Field(description="不明な餌の量")
    cant_hour: list[int] = Field(description="時間ごとの不明な餌の量")
    chacha: int = Field(description="チャチャが食べた餌の量")
    chacha_average: int = Field(description="指定した期間の日毎のチャチャの餌を食べた平均量")
    chacha_esaryo_by_ratio: int = Field(description="指定した期間の日毎のチャチャの餌を食べたトータル量")
    chacha_hour: list[int] = Field(description="時間ごとのチャチャの餌の量")
    chacha_ratio: int = Field(description="チャチャの餌の比率（パーセント）")
    day_count: int = Field(description="日数")
    kuro: int = Field(description="クロが食べた餌の量")
    kuro_average: int = Field(description="指定した期間の日毎のクロの餌を食べた平均量")
    kuro_esaryo_by_ratio: int = Field(description="指定した期間の日毎のクロの餌を食べたトータル量")
    kuro_hour: list[int] = Field(description="時間ごとのクロの餌の量")
    kuro_ratio: int = Field(description="クロの餌の比率（パーセント）")
    total: int = Field(description="指定した期間のチャチャとクロをあわせたトータル餌の量")

class NekoesaDataByDate(BaseModel):
    cant: int = Field(description="不明な餌の量")
    cant_hour: list[int] = Field(description="時間ごとの不明な餌の量")
    chacha: int = Field(description="チャチャが食べた餌の量")
    chacha_esaryo_by_ratio: int = Field(description="特定の日付の日毎のチャチャの餌を食べたトータル量")
    chacha_hour: list[int] = Field(description="時間ごとのチャチャの餌の量")
    chacha_ratio: int = Field(description="チャチャの餌の比率（パーセント）")
    kuro: int = Field(description="クロが食べた餌の量")
    kuro_esaryo_by_ratio: int = Field(description="特定の日付の日毎のクロの餌を食べたトータル量")
    kuro_hour: list[int] = Field(description="時間ごとのクロの餌の量")
    kuro_ratio: int = Field(description="クロの餌の比率（パーセント）")
    total: int = Field(description="特定の日付のチャチャとクロをあわせたトータル餌の量")

class NekoesaDateListItem(BaseModel):
    data: NekoesaDataByDate = Field(description="特定の日付のデータ")
    date: str = Field(description="日付の文字列（YYYYMMDD形式）")

class NEKOESA_INFO(BaseModel):
    data: NekoesaDataInfo = Field(description="指定した期間のチャチャとクロの餌を食べた量のまとめデータ")
    date_list: list[NekoesaDateListItem] = Field(description="指定した期間の日付リスト")

@mcp.tool()
def get_nekoesa_info(
    start: int = Field(description="検索を開始する日付。YYYYMMDD形式のintで指定する"),
    end: int = Field(description="検索を終了する日付。YYYYMMDD形式のintで指定する"),
) -> NEKOESA_INFO:
    """
    startとendで指定した期間の猫であるチャチャとクロ二匹のそれぞれの食べた餌の量を取得する。
    単位はグラム。
    猫はチャチャとクロの二匹なので、それぞれの餌の量を足したものがトータルの餌の量になる。
    チャチャはチャチ、チャツネとも呼ばれる。
    クロはクヨとも呼ばれる。
    """
    r = httpx.get(
        url=BASE_URL + f"/feedapi",
        params={"start": start, "end": end}
    )
    r.raise_for_status()
    return NEKOESA_INFO.model_validate(r.json())


def run():
    mcp.run()
