#include <iostream>
#include <cstdio>

#include "des.h"

using namespace std;

int main(int argc, char** argv){
  uint64_t in=0xfeed1337bead8787; //0xdeadbeef0feedbad;
  uint64_t key=0x0E329232EA6D0D73;//0x0113151911519101;
  uint64_t out1=encrypt(in, key);
  uint64_t out2=decrypt(out1, key);
  assert(in==out2);
  return 0;
}