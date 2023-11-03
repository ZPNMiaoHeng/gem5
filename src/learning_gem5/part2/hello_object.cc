#include "learning_gem5/part2/hello_object.hh"
#include "base/trace.hh"
#include "debug/HelloExample.hh"

#include <iostream>

namespace gem5
{
    HelloObject::HelloObject(const HelloObjectParams &params) :
        SimObject(params), event([this]{processEvent();}, name()),
        latency(100), timesLeft(10)
        {     // event可以执行任何函数，通过this捕捉并调用其中内容
 //           std::cout << "Hello World! From a SimObject!" << std::endl;
            DPRINTF(HelloExample, "Created the hello object\n");
        }

    // void 
    //     HelloObject::processEvent()
    //     {
    //         DPRINTF(HelloExample, "Hello world! Processing the event!\n");
    //     }

    void
        HelloObject::startup()
        {
            schedule(event, latency);    //：cppschedule函数,只允许调度在未来某个时间。
        }

    void
    HelloObject::processEvent()
    {
        timesLeft--;
        DPRINTF(HelloExample, "Hello world! Processing the event! %d left\n", timesLeft);

        if (timesLeft <= 0) {
            DPRINTF(HelloExample, "Done firing!\n");
        } else {
            schedule(event, curTick() + latency);
        }
    }
} // namespace gem5
