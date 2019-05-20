//
// Created by kwint on 26-4-19.
//

#include "seal_act.h"
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <threemxl/C3mxlROS.h>
#include <std_srvs/Trigger.h>

const double SEAL_POS_OPEN      = 0.201;
const double SEAL_POS_CLOSE     = 0.0297;
const double NIP_ROL_TRAVEL     = 0.5;


class SealAct{
protected:
    ros::NodeHandle n;
    ros::ServiceServer closeSeal_serv;
    ros::ServiceServer openSeal_serv;
    ros::ServiceServer nipRolDown_serv;
    C3mxl *seal_motor, *nip_motor;
    LxSerial serial_port; ///< Serial port interface


public:
    SealAct() : n("~") {
        seal_motor = new C3mxl();
        nip_motor = new C3mxl();

        CDxlConfig *config = new CDxlConfig();

        serial_port.port_open("/dev/ttyUSB0", LxSerial::RS485_FTDI);
        serial_port.set_speed(LxSerial::S921600);

        seal_motor->setSerialPort(&serial_port);
        seal_motor->setConfig(config->setID(100));
        seal_motor->init(false);

        nip_motor->setSerialPort(&serial_port);
        nip_motor->setConfig(config->setID(101));
        nip_motor->init(false);

//        ros::Rate loop(10);
//        seal_motor->set3MxlMode(EXTERNAL_INIT);
//        while (ros::ok())
//        {
//            // Check for status
//            seal_motor->getStatus();
//            if (seal_motor->presentStatus() != M3XL_STATUS_INITIALIZE_BUSY)
//            {
//                break;
//            }
//
//            loop.sleep();
//        }
//
//        if (seal_motor->presentStatus() != M3XL_STATUS_INIT_DONE)
//        {
//            ROS_FATAL_STREAM("Couldn't initialize seal motor: " << seal_motor->translateErrorCode(seal_motor->presentStatus()));
//            ROS_ISSUE_BREAK();
//        }

        nip_motor->set3MxlMode(POSITION_MODE);
        seal_motor->set3MxlMode(POSITION_MODE);

        closeSeal_serv = n.advertiseService("closeSeal", &SealAct::closeSeal, this);
        openSeal_serv = n.advertiseService("openSeal", &SealAct::openSeal, this);

        nipRolDown_serv = n.advertiseService("nipRolDown", &SealAct::nipRolDown, this);

    }

    bool closeSeal(std_srvs::TriggerRequest& request, std_srvs::TriggerResponse& response){
        goToPos(SEAL_POS_CLOSE, seal_motor);
        if (waitForMotor(seal_motor)){
            response.success = true;
            response.message = "";
            ROS_INFO("Sealer closed");
        }
        else{
            response.success = false;
            response.message = C3mxl::translateErrorCode(seal_motor->presentStatus());
            ROS_WARN("Closing sealer failed %s", C3mxl::translateErrorCode(seal_motor->presentStatus()));
        }
        return true;
    }

    bool openSeal(std_srvs::TriggerRequest& request, std_srvs::TriggerResponse& response){
        goToPos(SEAL_POS_OPEN, seal_motor);
        if (waitForMotor(seal_motor)){
            response.success = true;
            response.message = "";
            ROS_INFO("Sealer opened");
        }
        else{
            response.success = false;
            response.message = C3mxl::translateErrorCode(seal_motor->presentStatus());
            ROS_WARN("Opening sealer failed %s", C3mxl::translateErrorCode(seal_motor->presentStatus()));

        }
        return true;
    }

    bool nipRolDown(std_srvs::TriggerRequest& request, std_srvs::TriggerResponse& response){
        nip_motor->getLinearPos();
        goToPos(NIP_ROL_TRAVEL + nip_motor->presentLinearPos(), nip_motor);
        ROS_INFO("NIP ROLLING");
        response.success = true;
        response.message = "";
        return true;
    }

    void goToPos(double pos, C3mxl *motor){
        motor->setLinearPos(pos, false);
    }

    bool waitForMotor(C3mxl *motor){
        double start_time = ros::Time::now().toSec();
        ros::Rate checkRate(10);

        do {
            motor->getStatus();

            if((ros::Time::now().toSec() - start_time) > 10){
                ROS_WARN("Motor TIMEOUT");
                return false;
            }

            checkRate.sleep();

        } while (motor->presentStatus() != M3XL_STATUS_POS_MODE_DONE);

        if (0x80 < motor->presentStatus() && motor->presentStatus() < 0x89) {
            ROS_INFO("Motor action did not go well. %s", C3mxl::translateErrorCode(motor->presentStatus()));
            return false;
        }
        if (motor->presentStatus() == M3XL_STATUS_POS_MODE_DONE){
            ROS_INFO("Motor arrived at position");
            return true;
        }
    }

    void spin(){
        ros::Rate r(10);
        while(ros::ok()){
            ros::spin();
        }
    }

};

int main(int argc, char **argv) {
    ros::init(argc, argv, "seal_act");

    SealAct sealact;

    sealact.spin();
}
