import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets("tmp/data",one_hot=True)
import pylab

tf.reset_default_graph()
#定义占位符
x=tf.placeholder(tf.float32,[None,784])#图片为28*28
y=tf.placeholder(tf.float32,[None,10])#数字0~9
#定义学习参数
W=tf.Variable(tf.random_normal(([784,10])))
b=tf.Variable(tf.zeros([10]))
#定义输出结点
pred=tf.nn.softmax(tf.matmul(x,W)+b)#softmax分类
#定义反向传播
    #损失函数
cost=tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred),reduction_indices=1))
    #定义参数
learning_rate=0.01
    #使用梯度下降
optimizer=tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

training_epochs=25#训练集迭代次数
batch_size=100#每次取100个样本训练
display_step=1

saver=tf.train.Saver()
model_path="log/SingleModel.cpkt"
#启动session
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    #启动循环开始训练
    for epoch in range(training_epochs):
        avg_cost=0.
        total_batch=int(mnist.train.num_examples/batch_size)
        #循环所有数据
        for i in range(total_batch):
            batch_xs,batch_ys=mnist.train.next_batch(batch_size)
            #运行优化器
            _,c=sess.run([optimizer,cost],feed_dict={x:batch_xs,y:batch_ys})
            #计算平均loss
            avg_cost+=c/total_batch
        #显示训练信息
        if (epoch+1)%display_step==0:
            print("Epoch:","%04d"%(epoch+1),"cost=","{:.9f}".format(avg_cost))
    print("Finished!")
    #保存模型
    save_path=saver.save(sess,model_path)
    print("Model saved in file:%s"%save_path)
    #测试模型
    correct_prediction=tf.equal(tf.argmax(pred,1),tf.argmax(y,1))
        #计算准确率
    accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    print("Accuracy:",accuracy.eval({x:mnist.test.images,y:mnist.test.labels}))

    output=tf.argmax(pred,1)
    batch_xs,batch_ys=mnist.train.next_batch(2)
    outputval,predV=sess.run([output,pred],feed_dict={x:batch_xs})
    print(outputval,predV,batch_ys)#预测结果，预测得到的真实输出值、onehot编码

    im=batch_xs[0]
    im=im.reshape(-1,28)
    pylab.imshow(im)
    pylab.show()

    im=batch_xs[1]
    im=im.reshape(-1,28)
    pylab.imshow(im)
    pylab.show()

