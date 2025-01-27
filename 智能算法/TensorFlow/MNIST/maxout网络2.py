#本代码为课本样例，但是W2、b2并没有得到更新
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("tmp/data")
print ('输入数据:',mnist.train.images)
print ('输入数据打shape:',mnist.train.images.shape)
import pylab
im = mnist.train.images[1]
im = im.reshape(-1,28)
pylab.imshow(im)
pylab.show()
print ('输入数据打shape:',mnist.test.images.shape)
print ('输入数据打shape:',mnist.validation.images.shape)
import tensorflow as tf #导入tensorflow库
tf.reset_default_graph()
# tf Graph Input
x = tf.placeholder(tf.float32, [None, 784]) # mnist data维度 28*28=784
y = tf.placeholder(tf.int32, [None]) # 0-9 数字=> 10 classes
# Set model weights
W = tf.Variable(tf.random_normal([784, 10]))
b = tf.Variable(tf.zeros([10]))
z= tf.matmul(x, W) + b
maxout = tf.reduce_max(z,axis= 1,keep_dims=True)
# Set model weights
W2 = tf.Variable(tf.truncated_normal([1, 10], stddev=0.1))
b2 = tf.Variable(tf.zeros([1]))
# 构建模型
pred = tf.nn.softmax(tf.matmul(maxout, W2) + b2)
# 构建模型
#pred = tf.nn.softmax(z) # Softmax分类
# Minimize error using cross entropy
#cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
cost = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=z))
#参数设置
learning_rate = 0.04
# 使用梯度下降优化器
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
training_epochs = 50
batch_size = 100
display_step = 1
# 启动session
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())# Initializing OP
    # 启动循环开始训练
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        # 遍历全部数据集
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                          y: batch_ys})
            # Compute average loss
            avg_cost += c / total_batch
        # 显示训练中的详细信息
        if (epoch+1) % display_step == 0:
            print ("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))
            print("W=", sess.run(W), "b=", sess.run(b), "W2=", sess.run(W2), "b2=", sess.run(b2))
