
from operator import le
from typing import TypeVar

from numpy import outer


class DnsResponse:
    def __init__(self, bytes, comment="") -> None:
        self.index = 0
        self.bytes = bytes
        self.comment = comment

        self.transaction_id = self.read(2)
        self.direction = self.read_bit_sequence([
            1, 
            4,
            1,
            1,
            1,
        ])
        self.request_type = "response" if self.direction[0]  == "1" else "request"
        self.question_count = int.from_bytes(self.read(2), "big") 
        self.answer_count = int.from_bytes(self.read(2), "big") 
        self.recursive_count = int.from_bytes(self.read(2), "big") 
        self.additional_records = int.from_bytes(self.read(2), "big") 

        self.questions = self.read_question_section(self.question_count)
        self.answers = self.read_answer_section(self.answer_count)

    def read_bit_sequence(self, sequence):
        assert sum(sequence) == 8
        value =  "{0:b}".format(self.bytes[self.index])
        self.index += 1
        response = []
        index = 0
        for i in sequence:
            val = value[index:index+i]
            if len(val) == 0:
                response.append("0")
            else:
                response.append(val)
            index += i
        self.index += 1
        return response

    def read(self, length):
        response = self.peek(length)
        self.index += length
        return response
    
    def peek(self, length):
        return self.bytes[self.index:self.index + length]

    def read_question_section(self, count):
        output = []
        for _ in range(count):
            output.append(self.parse_question_entry())
        return output

    def read_answer_section(self, count):
        output = []
        for _ in range(count):
            output.append(self.parse_answer_entry())
        return output

    def parse_question_entry(self):
        name = self.read_out_name()
        type_value = self.read(2)
        class_value = self.read(2)

        return (
            name,
            type_value,
            class_value,
        )

    def parse_answer_entry(self):
        name = self.read(2)
        type_value = self.read(2)
        class_value = self.read(2)
        ttl = self.read(4)
        data_length = int.from_bytes(self.read(2), "big")
        data = ".".join(list(map(lambda x: str(int(x)), self.read(data_length))))
        return (
            name,
            type_value,
            class_value,
            ttl,
            data
        )

    def read_out_name(self):
        name = bytes([])
        while True:
            length = int.from_bytes(self.peek(1), "big")
            if length == 0:
                self.index += 1
                break
            self.index += 1
            name += bytes([ord(".")]) if len(name) > 0 else bytes([])
            name += self.read(length)
        return name
    
    def __str__(self) -> str:
        return """
            {comment}
            transaction_id: {transaction_id}
            direction : {direction}
            request_type: {request_type}
            question_count: {question_count}
            answer_count: {answer_count}
            recursive_count: {recursive_count}
            additional_records: {additional_records}
        """.format(
            comment=self.comment,
            transaction_id=self.transaction_id,
            direction=self.direction,
            request_type=self.request_type,
            question_count=self.question_count,
            answer_count=self.answer_count,
            recursive_count=self.recursive_count,
            additional_records=self.additional_records,
        )
    
    def __repr__(self) -> str:
        return self.__str__()
