"""
MVSV 文件解析器

MVSV（Metadata Vertical bar Separated Values）格式文件的解析器，
用于将 MVSV 文件解析为结构化的 MVSVData 对象。

@author: ACANX
@since: 2026-05-21
"""

from dataclasses import dataclass, field as dc_field
from typing import List, Dict, Optional


@dataclass
class MVSVMetadata:
    """MVSV 文件元数据"""
    title: str = ""
    title_en: Optional[str] = None
    data_provider: str = ""
    data_provider_en: Optional[str] = None
    fields: str = ""  # 使用 fields 替代 field 避免与 dataclass.field 冲突
    fields_en: Optional[str] = None
    field_name: str = ""
    field_name_en: Optional[str] = None
    field_type: str = ""
    field_type_en: Optional[str] = None
    count: int = 0
    remark: Optional[str] = None
    remark_en: Optional[str] = None
    extra: Dict[str, str] = dc_field(default_factory=dict)

    def get_field_list(self) -> List[str]:
        """获取字段名列表"""
        if not self.fields:
            return []
        return self.fields.split('|')

    def get_field_name_list(self) -> List[str]:
        """获取字段中文名称列表"""
        if not self.field_name:
            return []
        return self.field_name.split('|')

    def get_field_type_list(self) -> List[str]:
        """获取字段类型列表"""
        if not self.field_type:
            return []
        return self.field_type.split('|')


@dataclass
class MVSVData:
    """MVSV 文件数据"""
    metadata: MVSVMetadata
    headers: Optional[List[str]] = None  # 无元数据时为 None
    field_names: List[str] = dc_field(default_factory=list)
    field_types: List[str] = dc_field(default_factory=list)
    rows: List[List[str]] = dc_field(default_factory=list)


class MVSVParser:
    """MVSV 文件解析器"""

    def parse(self, file_path: str) -> MVSVData:
        """
        解析 MVSV 文件

        Args:
            file_path: 文件路径

        Returns:
            解析后的数据对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 解析元数据区
        metadata = self._parse_metadata(lines)

        # 解析数据区
        rows = self._parse_data(lines)

        # 从元数据获取 headers，无元数据时 headers 为 None
        headers = None
        if metadata.fields:
            headers = metadata.get_field_list()

        # 解析字段名称和类型
        field_names = metadata.get_field_name_list()
        field_types = metadata.get_field_type_list()

        return MVSVData(
            metadata=metadata,
            headers=headers,
            field_names=field_names,
            field_types=field_types,
            rows=rows
        )

    def parse_string(self, content: str) -> MVSVData:
        """
        从字符串解析 MVSV 数据

        Args:
            content: MVSV 内容字符串

        Returns:
            解析后的数据对象
        """
        lines = content.split('\n')

        # 解析元数据区
        metadata = self._parse_metadata(lines)

        # 解析数据区
        rows = self._parse_data(lines)

        # 从元数据获取 headers，无元数据时 headers 为 None
        headers = None
        if metadata.fields:
            headers = metadata.get_field_list()

        # 解析字段名称和类型
        field_names = metadata.get_field_name_list()
        field_types = metadata.get_field_type_list()

        return MVSVData(
            metadata=metadata,
            headers=headers,
            field_names=field_names,
            field_types=field_types,
            rows=rows
        )

    def _parse_metadata(self, lines: List[str]) -> MVSVMetadata:
        """解析元数据区"""
        metadata = {}

        for line in lines:
            line = line.strip()
            if not line.startswith('#'):
                break

            # 解析字段：# 字段名 : 字段值
            if ' : ' in line:
                key_value = line[2:].split(' : ', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    # 去除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    metadata[key] = value

        return MVSVMetadata(
            title=metadata.get('标题', ''),
            title_en=metadata.get('Title'),
            data_provider=metadata.get('数据供应商', ''),
            data_provider_en=metadata.get('DataProvider'),
            fields=metadata.get('字段', ''),
            fields_en=metadata.get('Field'),
            field_name=metadata.get('字段名称', ''),
            field_name_en=metadata.get('FieldName'),
            field_type=metadata.get('字段类型', ''),
            field_type_en=metadata.get('FieldType'),
            count=int(metadata.get('计数', metadata.get('Count', 0))),
            remark=metadata.get('备注'),
            remark_en=metadata.get('Remark'),
            extra=metadata
        )

    def _parse_data(self, lines: List[str]) -> List[List[str]]:
        """解析数据区"""
        rows = []

        for line in lines:
            line = line.strip()

            # 跳过注释行和空行
            if line.startswith('#') or not line:
                continue

            # 数据行
            if '|' in line:
                values = line.split('|')
                rows.append(values)

        return rows
