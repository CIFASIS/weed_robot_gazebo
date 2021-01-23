#ifndef _WORLD_ODOM_PUBLISHER_HH_
#define _WORLD_ODOM_PUBLISHER_HH_

#include <functional>
#include <gazebo/gazebo.hh>
#include <ignition/math/Pose3.hh>
#include <ignition/math/Vector3.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>
#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>

using namespace gazebo;

class WorldOdomPublisher : public ModelPlugin {

    private: physics::ModelPtr model;
    private: event::ConnectionPtr updateConnection;
    private: std::unique_ptr<ros::NodeHandle> node;
    private: ros::Publisher pub;
    private: tf::TransformBroadcaster tf;

    private: ros::Time lastTime;

    private: double publishFreq = 10.0; // publish_frequency

    public: void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf) {

        if (_sdf->HasElement("world_odom")) {
            std::cout << "Se utiliza la odometría real del robot.\n";
        } else {
            std::cout << "Se utiliza la odometría del controlador.\n";
        }

        if (_sdf->HasElement("publish_frequency")) {
            publishFreq = _sdf->Get<double>("publish_frequency");
        }

        model = _model;

        updateConnection = event::Events::ConnectWorldUpdateBegin(
                std::bind(&WorldOdomPublisher::OnUpdate, this));

        lastTime = ros::Time::now();

        // initialize ros
        std::string ns = "world_odom_publisher";
        if (!ros::isInitialized()) {
            int argc = 0;
            char **argv = NULL;
            ros::init(argc, argv, ns, ros::init_options::NoSigintHandler);
        }
        node.reset(new ros::NodeHandle(ns));

        pub = node->advertise<nav_msgs::Odometry>("odom", 50);

    }

    public: void OnUpdate() {

        ros::Time currentTime = ros::Time::now();

        double deltaSecs = currentTime.toSec() - lastTime.toSec();

        double maxSecs = 0.0;
        if (publishFreq != 0.0) {
            maxSecs = 1.0 / publishFreq;
        }

        if (deltaSecs > maxSecs && deltaSecs != 0.0) {
            lastTime = currentTime;
            PublishOdom(currentTime);
        }
    }

    private: void PublishOdom(ros::Time& currentTime) {

        ignition::math::Pose3d pose = model->WorldPose();
        double x = pose.Pos().X();
        double y = pose.Pos().Y();
        double th = pose.Rot().Yaw();

        ignition::math::Vector3d linearVel = model->WorldLinearVel();
        double vx = linearVel.X();
        double vy = linearVel.Y();

        ignition::math::Vector3d angularVel = model->WorldAngularVel();
        double vth = angularVel.Z();

//        std::cout << "Pose: [x=" << x << ", y=" << y << ", th=" << th << "]\n";
//        std::cout << "Twist: [vx=" << vx << ", vy=" << vy << ", vth=" << vth << "]\n";

        geometry_msgs::Quaternion q = tf::createQuaternionMsgFromYaw(th);

        // transformation frame
        geometry_msgs::TransformStamped ts;
        ts.header.stamp = currentTime;
        ts.header.frame_id = "odom";
        ts.child_frame_id = "base_link";

        ts.transform.translation.x = x;
        ts.transform.translation.y = y;
        ts.transform.translation.z = 0.0;
        ts.transform.rotation = q;

        tf.sendTransform(ts);

        // publish odometry topic
        nav_msgs::Odometry odom;
        odom.header.stamp = currentTime;
        odom.header.frame_id = "odom";
        odom.child_frame_id = "base_link";

        odom.pose.pose.position.x = x;
        odom.pose.pose.position.y = y;
        odom.pose.pose.position.z = 0.0;
        odom.pose.pose.orientation = q;

        odom.twist.twist.linear.x = vx;
        odom.twist.twist.linear.y = vy;
        odom.twist.twist.angular.z = vth;

        pub.publish(odom);
    }

};

GZ_REGISTER_MODEL_PLUGIN(WorldOdomPublisher)
#endif
