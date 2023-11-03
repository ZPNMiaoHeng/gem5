#ifndef __LEARNING_GEM5_HELLO_OBJECT_HH__
#define __LEARNING_GEM5_HELLO_OBJECT_HH__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

namespace gem5
{

    class HelloObject : public SimObject
    {
        private:
            void processEvent();          // 定义的函数

            EventFunctionWrapper event;   // 执行任何函数，需要两个参数

            const Tick latency;
            
            int timesLeft;

        public:
            HelloObject(const HelloObjectParams &p);

            void startup() override;
    };

} // namespace gem5

#endif // __LEARNING_GEM5_HELLO_OBJECT_HH__
