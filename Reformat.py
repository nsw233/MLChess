import sys

raw_data_name = sys.argv[1]
f_raw = file(raw_data_name,'r')
raw_data = f_raw.read().split('\n')
out_data_name = sys.argv[2]
f_out = file(out_data_name,'w')

def LinReg(val):
  num_str,den_str = val.split('/')
  num = int(num_str)
  den = int(den_str)
  if num > 0:
    return .1 + (.9*num)/den
  else:
    return -.1 + (.9*num)/den

def ConstReg(val):
  num_str, den_str = val.split('/')
  num = int(num_str)
  if num > 0:
    return 1
  else:
    return -1

def NoAgg(data):
  return [float(datum) for datum in data]

def Agg(data):
  data = [float(datum) for datum in data]
  w_1 = sum(data[:2])
  w_2 = sum(data[2:18])
  w_3 = sum(data[18:34])
  w_4 = sum(data[34:66])
  b_1 = sum(data[66:68])
  b_2 = sum(data[68:84])
  b_3 = sum(data[84:100])
  b_4 = sum(data[100:132])
  return [w_1,w_2,w_3,w_4,b_1,b_2,b_3,b_4]

for line in raw_data:
  if not line:
    continue
  out_str = ''
  line_data = line.split(' ')
  val = ConstReg(line_data[0])
  feats = Agg(line_data[1:])
  out_str += str(val)
  for i, feat in enumerate(feats):
    out_str += ' ' + str(i+1) + ':' + str(feat)
  out_str += '\n'
  f_out.write(out_str)

