"""
MVSV 格式解析器单元测试

@author: ACANX
@since: 2026-05-21
"""

import os
import tempfile
import unittest

from metax.base.file.mvsv_parser import MVSVParser, MVSVMetadata, MVSVData
from metax.base.file.mvsv_serializer import MVSVSerializer


# 测试数据
TEST_MVSV_CONTENT = """# 标题 : "黄金分钟级行情 - 2026-05-21"
# Title : "Gold Minute-level Quotes - 2026-05-21"
# 数据供应商 : xxx行情采集程序
# DataProvider : xxx Quote Collector
# 字段 : Timestamp|Open|High|Low|Close|Volume
# Field : Timestamp|Open|High|Low|Close|Volume
# 字段名称 : 时间戳|开盘|最高|最低|收盘|成交量
# FieldName : 时间戳|开盘|最高|最低|收盘|成交量
# 字段类型 : timestamp|number|number|number|number|integer
# FieldType : timestamp|number|number|number|number|integer
# 计数 : 3
# Count : 3
# 时区 : Asia/Shanghai
# Timezone : Asia/Shanghai
# 货币 : CNY
# Currency : CNY
# 单位 : 元/克
# Unit : CNY/g
# 备注 : "开盘2345.00 收盘2350.00"
# Remark : "Open 2345.00 Close 2350.00"

09:00|2345.00|2350.00|2340.00|2348.50|12345
09:01|2348.50|2352.00|2347.00|2351.00|13456
09:02|2351.00|2355.00|2350.00|2353.50|14567"""

# 测试纯数据（无元数据）
TEST_PURE_DATA_CONTENT = """Timestamp|Open|High|Low|Close|Volume
09:00|2345.00|2350.00|2340.00|2348.50|12345
09:01|2348.50|2352.00|2347.00|2351.00|13456"""

# 测试空值处理
TEST_NULL_VALUE_CONTENT = """# 字段 : Timestamp|Open|High|Low|Close|Volume
# Field : Timestamp|Open|High|Low|Close|Volume

09:00|2345.00|2350.00||2348.50|12345
09:01|2348.50||2347.00|2351.00|13456"""


class MVSVParserTest(unittest.TestCase):

    def test_parse_string(self):
        """测试从字符串解析"""
        parser = MVSVParser()
        data = parser.parse_string(TEST_MVSV_CONTENT)

        # 验证基本解析
        self.assertEqual("黄金分钟级行情 - 2026-05-21", data.metadata.title)
        self.assertEqual(3, len(data.rows))

    def test_parse_file(self):
        """测试从文件解析"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mvsv', delete=False, encoding='utf-8') as f:
            f.write(TEST_MVSV_CONTENT)
            temp_path = f.name

        try:
            parser = MVSVParser()
            data = parser.parse(temp_path)

            # 验证基本解析
            self.assertEqual("黄金分钟级行情 - 2026-05-21", data.metadata.title)
            self.assertEqual(3, len(data.rows))
        finally:
            os.unlink(temp_path)

    def test_parse_pure_mvsv_data(self):
        """测试纯数据解析（无元数据）"""
        parser = MVSVParser()
        data = parser.parse_string(TEST_PURE_DATA_CONTENT)

        # 验证无元数据时解析正常
        self.assertEqual("", data.metadata.title)

        # 无元数据时，headers 为 None
        self.assertIsNone(data.headers)

        # 所有行都是数据（3行）
        self.assertEqual(3, len(data.rows))

    def test_parse_null_value(self):
        """测试空值处理"""
        parser = MVSVParser()
        data = parser.parse_string(TEST_NULL_VALUE_CONTENT)

        # 验证空值处理
        self.assertEqual(2, len(data.rows))

        # 第一行 Low 字段为空
        self.assertEqual("", data.rows[0][3])

        # 第二行 High 字段为空
        self.assertEqual("", data.rows[1][2])

    def test_metadata_get_methods(self):
        """测试元数据获取方法"""
        metadata = MVSVMetadata()
        metadata.fields = "A|B|C|D"
        metadata.field_name = "名称A|名称B|名称C|名称D"
        metadata.field_type = "string|number|integer|boolean"

        # 测试 get_field_list
        field_list = metadata.get_field_list()
        self.assertEqual(4, len(field_list))

        # 测试 get_field_name_list
        field_name_list = metadata.get_field_name_list()
        self.assertEqual(4, len(field_name_list))

        # 测试 get_field_type_list
        field_type_list = metadata.get_field_type_list()
        self.assertEqual(4, len(field_type_list))

        # 测试空值情况
        empty_metadata = MVSVMetadata()
        self.assertEqual([], empty_metadata.get_field_list())
        self.assertEqual([], empty_metadata.get_field_name_list())
        self.assertEqual([], empty_metadata.get_field_type_list())

    def test_chinese_english_metadata(self):
        """测试中英双语元数据解析"""
        content = """# 标题 : "中文标题"
# Title : "English Title"
# 字段 : A|B|C
# Field : A|B|C

1|2|3"""
        parser = MVSVParser()
        data = parser.parse_string(content)

        self.assertEqual("中文标题", data.metadata.title)
        self.assertEqual("English Title", data.metadata.title_en)
        self.assertEqual("A|B|C", data.metadata.fields)
        self.assertEqual("A|B|C", data.metadata.fields_en)

    def test_serialize_to_string(self):
        """测试序列化为字符串"""
        metadata = MVSVMetadata(
            title="测试标题",
            title_en="Test Title",
            fields="A|B|C",
            fields_en="A|B|C",
            field_name="字段A|字段B|字段C",
            field_type="string|number|integer",
            count=2,
            remark="测试备注",
            remark_en="Test Remark"
        )
        data = MVSVData(
            metadata=metadata,
            headers=["A", "B", "C"],
            field_names=["字段A", "字段B", "字段C"],
            field_types=["string", "number", "integer"],
            rows=[["1", "2", "3"], ["4", "5", "6"]]
        )

        serializer = MVSVSerializer()
        result = serializer.serialize_to_string(data)

        # 验证序列化结果
        self.assertIn('# 标题 : "测试标题"', result)
        self.assertIn('# Title : "Test Title"', result)
        self.assertIn('# 字段 : A|B|C', result)
        self.assertIn('# Field : A|B|C', result)
        self.assertIn('1|2|3', result)
        self.assertIn('4|5|6', result)

    def test_serialize_to_file(self):
        """测试序列化到文件"""
        metadata = MVSVMetadata(
            title="测试标题",
            fields="A|B|C",
            count=1
        )
        data = MVSVData(
            metadata=metadata,
            headers=["A", "B", "C"],
            rows=[["1", "2", "3"]]
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.mvsv', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            serializer = MVSVSerializer()
            serializer.serialize(data, temp_path)

            # 读取并验证
            parser = MVSVParser()
            parsed_data = parser.parse(temp_path)

            self.assertEqual("测试标题", parsed_data.metadata.title)
            self.assertEqual("A|B|C", parsed_data.metadata.fields)
            self.assertEqual(1, len(parsed_data.rows))
        finally:
            os.unlink(temp_path)

    def test_roundtrip(self):
        """测试解析后序列化再解析"""
        # 原始解析
        parser = MVSVParser()
        original_data = parser.parse_string(TEST_MVSV_CONTENT)

        # 序列化
        serializer = MVSVSerializer()
        serialized = serializer.serialize_to_string(original_data)

        # 再次解析
        reparsed_data = parser.parse_string(serialized)

        # 验证数据一致性
        self.assertEqual(original_data.metadata.title, reparsed_data.metadata.title)
        self.assertEqual(len(original_data.rows), len(reparsed_data.rows))


if __name__ == '__main__':
    unittest.main()