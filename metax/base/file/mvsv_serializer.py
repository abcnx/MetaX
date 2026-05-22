"""
MVSV 文件序列化器

MVSV（Metadata Vertical bar Separated Values）格式文件的序列化器，
用于将 MVSVData 对象序列化为 MVSV 格式文件。

@author: ACANX
@since: 2026-05-21
"""

from typing import List, Optional

from metax.base.file.mvsv_parser import MVSVData, MVSVMetadata


class MVSVSerializer:
    """MVSV 文件序列化器"""

    def serialize(self, data: MVSVData, file_path: str) -> None:
        """
        序列化为 MVSV 文件

        Args:
            data: 数据对象
            file_path: 文件路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            # 写入元数据区
            self._write_metadata(f, data.metadata)

            # 写入空行分隔
            f.write('\n')

            # 写入数据区
            self._write_data(f, data.rows)

    def serialize_to_string(self, data: MVSVData) -> str:
        """
        序列化为字符串

        Args:
            data: 数据对象

        Returns:
            MVSV 格式字符串
        """
        builder = []

        # 写入元数据区
        self._write_metadata_to_builder(builder, data.metadata)

        # 写入空行分隔
        builder.append('')

        # 写入数据区
        self._write_data_to_builder(builder, data.rows)

        return '\n'.join(builder)

    def _write_metadata(self, f, metadata: MVSVMetadata) -> None:
        """写入元数据区"""
        # 中文元数据
        if metadata.title:
            f.write(f'# 标题 : "{metadata.title}"\n')
        if metadata.data_provider:
            f.write(f'# 数据供应商 : {metadata.data_provider}\n')
        if metadata.fields:
            f.write(f'# 字段 : {metadata.fields}\n')
        if metadata.field_name:
            f.write(f'# 字段名称 : {metadata.field_name}\n')
        if metadata.field_type:
            f.write(f'# 字段类型 : {metadata.field_type}\n')
        if metadata.count:
            f.write(f'# 计数 : {metadata.count}\n')
        if metadata.remark:
            f.write(f'# 备注 : "{metadata.remark}"\n')

        # 英文元数据
        if metadata.title_en:
            f.write(f'# Title : "{metadata.title_en}"\n')
        if metadata.data_provider_en:
            f.write(f'# DataProvider : {metadata.data_provider_en}\n')
        if metadata.fields_en:
            f.write(f'# Field : {metadata.fields_en}\n')
        if metadata.field_name_en:
            f.write(f'# FieldName : {metadata.field_name_en}\n')
        if metadata.field_type_en:
            f.write(f'# FieldType : {metadata.field_type_en}\n')
        if metadata.count:
            f.write(f'# Count : {metadata.count}\n')
        if metadata.remark_en:
            f.write(f'# Remark : "{metadata.remark_en}"\n')

    def _write_data(self, f, rows: List[List[str]]) -> None:
        """写入数据区"""
        for row in rows:
            f.write('|'.join(str(v) for v in row) + '\n')

    def _write_metadata_to_builder(self, builder: list, metadata: MVSVMetadata) -> None:
        """写入元数据区到列表"""
        # 中文元数据
        if metadata.title:
            builder.append(f'# 标题 : "{metadata.title}"')
        if metadata.data_provider:
            builder.append(f'# 数据供应商 : {metadata.data_provider}')
        if metadata.fields:
            builder.append(f'# 字段 : {metadata.fields}')
        if metadata.field_name:
            builder.append(f'# 字段名称 : {metadata.field_name}')
        if metadata.field_type:
            builder.append(f'# 字段类型 : {metadata.field_type}')
        if metadata.count:
            builder.append(f'# 计数 : {metadata.count}')
        if metadata.remark:
            builder.append(f'# 备注 : "{metadata.remark}"')

        # 英文元数据
        if metadata.title_en:
            builder.append(f'# Title : "{metadata.title_en}"')
        if metadata.data_provider_en:
            builder.append(f'# DataProvider : {metadata.data_provider_en}')
        if metadata.fields_en:
            builder.append(f'# Field : {metadata.fields_en}')
        if metadata.field_name_en:
            builder.append(f'# FieldName : {metadata.field_name_en}')
        if metadata.field_type_en:
            builder.append(f'# FieldType : {metadata.field_type_en}')
        if metadata.count:
            builder.append(f'# Count : {metadata.count}')
        if metadata.remark_en:
            builder.append(f'# Remark : "{metadata.remark_en}"')

    def _write_data_to_builder(self, builder: list, rows: List[List[str]]) -> None:
        """写入数据区到列表"""
        for row in rows:
            builder.append('|'.join(str(v) for v in row))
