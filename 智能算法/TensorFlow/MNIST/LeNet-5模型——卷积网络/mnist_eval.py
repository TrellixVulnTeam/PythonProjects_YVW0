# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import time
import numpy as np

#加载mnist_inference.py和mnist_train.py中定义的常量和函数
import mnist_inference
import mnist_train

#每10秒加载一次最新的模型，并在测试数据上测试最新模型的正确率
EVAL_INTERVAL_SECS=10

def evaluate(mnist):
    with tf.Graph().as_default() as g:
        #定义输入输出的格式
        x = tf.placeholder(tf.float32, [mnist.validation.num_examples,  # 第一维表示一个batch中样例的个数
                                        mnist_inference.IMAGE_SIZE,  # 第二、三维表示图片尺寸
                                        mnist_inference.IMAGE_SIZE,
                                        mnist_inference.NUM_CHANNELS],  # 第四维表示图片的深度，对于RBG图片为5
                           name='x-input')
        y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name='y-input')
        validation_images_reshaped=np.reshape(mnist.validation.images,(mnist.validation.num_examples,
                                                                       mnist_inference.IMAGE_SIZE,
                                                                       mnist_inference.IMAGE_SIZE,
                                                                       mnist_inference.NUM_CHANNELS))
        validate_feed={x:validation_images_reshaped,y_:mnist.validation.labels}

        #直接通过调用封装好的函数计算前向传播结果
        #测试时不关注正则化损失的值，置为None
        y=mnist_inference.inference(x,False,None)

        #使用前向传播的结果计算正确率
        correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
        accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
        #当需要离线预测未知数据的类别时，将该部分改为答案输出

        #通过变量重命名的方式加载模型
        #这样不需要调用求滑动平均值的函数获取平均值，共用一个函数
        variable_averages=tf.train.ExponentialMovingAverage(
            mnist_train.MOVING_AVERAGE_DECAY
        )
        variables_to_restore=variable_averages.variables_to_restore()
        saver=tf.train.Saver(variables_to_restore)

        #每隔指定间隔调用一次计算正确率的过程以检测训练过程中正确率的变化
        while True:
            with tf.Session() as sess:
                gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.10)
                sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
                #tf.train.get_checkpoint_state函数会通过checkpoint文件自动找到目录中最新模型的文件名
                ckpt=tf.train.get_checkpoint_state(mnist_train.MODEL_SAVE_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    #加载模型
                    saver.restore(sess,ckpt.model_checkpoint_path)
                    #通过文件名得到模型保存时迭代的轮数
                    global_step=ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    accuracy_score=sess.run(accuracy,feed_dict=validate_feed)
                    print("After %s training step(s),validation "
                          "accuracy = %g."%(global_step,accuracy_score))
                else:
                    print('No checkpoint file found.')
                    return
            time.sleep(EVAL_INTERVAL_SECS)

def evaluate2(mnist):
    with tf.Graph().as_default() as g:
        #定义输入输出的格式
        x = tf.placeholder(tf.float32, [mnist.validation.num_examples,  # 第一维表示一个batch中样例的个数
                                        mnist_inference.IMAGE_SIZE,  # 第二、三维表示图片尺寸
                                        mnist_inference.IMAGE_SIZE,
                                        mnist_inference.NUM_CHANNELS],  # 第四维表示图片的深度，对于RBG图片为5
                           name='x-input')
        y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name='y-input')
        validation_images_reshaped=np.reshape(mnist.validation.images,(mnist.validation.num_examples,
                                                                       mnist_inference.IMAGE_SIZE,
                                                                       mnist_inference.IMAGE_SIZE,
                                                                       mnist_inference.NUM_CHANNELS))
        validate_feed={x:validation_images_reshaped,y_:mnist.validation.labels}

        #直接通过调用封装好的函数计算前向传播结果
        #测试时不关注正则化损失的值，置为None
        y=mnist_inference.inference(x,False,None)

        #使用前向传播的结果计算正确率
        correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
        accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
        #当需要离线预测未知数据的类别时，将该部分改为答案输出

        #通过变量重命名的方式加载模型
        #这样不需要调用求滑动平均值的函数获取平均值，共用一个函数
        variable_averages=tf.train.ExponentialMovingAverage(
            mnist_train.MOVING_AVERAGE_DECAY
        )
        variables_to_restore=variable_averages.variables_to_restore()
        saver=tf.train.Saver(variables_to_restore)
        with tf.Session() as sess:
            epoch=26000
            for i in range(5):
                saver.restore(sess,mnist_train.MODEL_SAVE_PATH+mnist_train.MODEL_NAME+"-"+str(epoch))
                global_step = epoch+i*1000
                accuracy_score = sess.run(accuracy, feed_dict=validate_feed)
                print("After %s training step(s),validation "
                        "accuracy = %.10f" % (global_step, accuracy_score))

def main(argv=None):
    mnist=input_data.read_data_sets('../tmp/data',one_hot=True)
    #evaluate(mnist)
    evaluate2(mnist)

if __name__=='__main__':
    tf.app.run()


