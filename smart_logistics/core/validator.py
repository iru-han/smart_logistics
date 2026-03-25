# smart_logistics/core/validator.py

class DataValidator:
    @staticmethod
    def validate(data, fields_schema):
        """
        :param data: dict { 'key': '입력값' }
        :param fields_schema: dict { 'key': ('이름', 타입) }
        """
        for key, (label, dtype) in fields_schema.items():
            value = str(data.get(key, "")).strip()
            
            # 1. 빈 값 체크
            if not value:
                return False, f"{label}를(을) 입력해주세요."
            
            # 2. 타입 변환 체크
            try:
                if dtype == float:
                    float(value)
                elif dtype == int:
                    int(value)
            except ValueError:
                return False, f"{label}의 형식이 올바르지 않습니다. (숫자 입력 필요)"

        return True, ""