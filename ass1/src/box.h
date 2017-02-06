#include <cassert>
#include <cstring>

class Data{
public:
  char *raw;
  size_t nbits;
  Data(size_t _nbits){
    raw = NULL;
    nbits = _nbits;
    alloc();
  }
  Data(const Data &b){
    nbits = b.nbits;
    auto sz = alloc();
    memcpy(raw, b.raw, sz);
  }
  Data(Data &&b){
    nbits = b.nbits;
    raw = b.raw;
    b.raw = NULL;
    b.nbits = 0;
  }
  size_t alloc(){
    size_t sz = 0;
    if(nbits)
    {
      sz = (nbits+7)/8; //allocate less than 1 extra byte.
      raw = new char[sz];
    }
    return sz;
  }
  char get_byte(size_t idx){
    assert(idx*8 < nbits);
    return raw[idx];
  }
  char get_bit(size_t idx){
    assert(idx < nbits);
    auto byte_idx = idx/8;
    return (raw[byte_idx] >> (idx % 8)) & 1;
  }
  //start, end in bits. end is not included in slice
  Data slice(size_t start, size_t end){
    assert(end <= nbits && start <= end);
    Data res(end-start);
    if(start % 8 == 0){
      memcpy(res.raw, raw + start/8, res.nbits/8);
    }else{
      for(auto idx = start;idx != end;idx++){
        res.raw.set_bit(idx - start, get_bit(idx));
      }
    }
  }
  ~Data(){
    delete []raw;
    raw = NULL;
    nbits = 0;
  }

};
class Box
{
  public:
    Data operator ()(const Data &input){
    }
};