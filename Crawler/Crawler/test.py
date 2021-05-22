update_version = ('iPhone', 'Pro', 'Max', 'Mini', 'Plus')
global_version = ('Quốc tế', 'Chính Hãng', 'VN/A', 'Nguyên Bản')
status = ('Cũ', 'Mới', 'Đã Kích Hoạt')
tests = ('iPhone 11 64GB Chính Hãng VN/A', 'iPhone 12 Pro Max 128GB Chính Hãng VN/A', 'iPhone 7 Plus Cũ 32Gb Nguyên Bản', 'iPhone 13 Pro Max', 'iPhone 13')

except_text = ('Quốc tế', 'Chính Hãng', 'VN/A', 'Nguyên Bản', 'Cũ', 'Mới', 'Đã Kích Hoạt')
result = []

for test in tests:
    getVals = list([val for val in test.split(" ")
                    if val in update_version or val.isnumeric()])
    result.append(" ".join(getVals))

print(result)
