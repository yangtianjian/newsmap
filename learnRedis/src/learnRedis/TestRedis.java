

import org.junit.Test;

import redis.clients.jedis.Jedis;

/**
 * Redis结合java的一个小demo
 *  转自：http://www.cnblogs.com/liuhongfeng/p/5033559.html,也可见菜鸟教程：
 *  http://www.runoob.com/redis/redis-java.html
 * Redis所以来的三个java：
 * commons-pool-1.6.jar
   jedis-2.1.0.jar
   tomcat-redis-session-manager-1.2-tomcat-7.jar
 * @author Wei
 * @time 2016年10月26日 下午2:35:02
 */
public class RedisJava {
    public static void main(String[] args) {
        // 连接本地的 Redis 服务
        Jedis jedis = new Jedis("localhost");
        System.out.println("连接本地的 Redis 服务成功！");
        // 查看服务是否运行
        System.out.println("服务 正在运行: " + jedis.ping());
    }
    @Test
    //Redis Java String(字符串) 实例
    public void TestRedisString(){
        //连接本地的 Redis 服务
          Jedis jedis = new Jedis("localhost");
          System.out.println("Connection to server sucessfully");
          //设置 redis 字符串数据
//          jedis.set("runoobkey", "Redis tutorial");
//         // 获取存储的数据并输出
//         System.out.println("Stored string in redis:: "+ jedis.get("runoobkey"));
         String name = jedis.get("theName");
         System.out.println("Stored theName in redis:: "+ name);
    }
    
    
}