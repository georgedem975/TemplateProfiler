import json

from pydantic import BaseModel, field_validator


class BenchmarkRecordSchema(BaseModel):
    id: int
    template_engine: str
    render_time_ms: str
    payload: str
    created_at: str

class BenchmarkRecordCreateSchema(BaseModel):
    template_engine: str
    render_time_ms: str
    payload: str


    @field_validator('template_engine')
    @classmethod
    def validate_template_engine(cls, v):
        allowed_engines = ['mustache', 'handlebars', 'lodash', 'ejs', 'nunjucks', 'eta']
        if v not in allowed_engines:
            raise ValueError(f'template_engine must be one of: {", ".join(allowed_engines)}')
        return v

    @field_validator('render_time_ms')
    @classmethod
    def validate_render_time_ms(cls, v):
        try:
            num_value = float(v)
            formatted = f"{num_value:.3f}"
            return formatted
        except ValueError:
            raise ValueError('render_time_ms must be an valid float in string format')

    @field_validator('payload')
    @classmethod
    def validate_payload(cls, v):
        try:
            json.loads(v)
            return v
        except json.JSONDecodeError:
            raise ValueError('payload must be valid JSON string')
