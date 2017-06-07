

import org.junit.Test;

import redis.clients.jedis.Jedis;

/**
 * Redis���java��һ��Сdemo
 *  ת�ԣ�http://www.cnblogs.com/liuhongfeng/p/5033559.html,Ҳ�ɼ�����̳̣�
 *  http://www.runoob.com/redis/redis-java.html
 * Redis������������java��
 * commons-pool-1.6.jar
   jedis-2.1.0.jar
   tomcat-redis-session-manager-1.2-tomcat-7.jar
 * @author Wei
 * @time 2016��10��26�� ����2:35:02
 */
public class RedisJava {
    public static void main(String[] args) {
        // ���ӱ��ص� Redis ����
        Jedis jedis = new Jedis("localhost");
        System.out.println("���ӱ��ص� Redis ����ɹ���");
        // �鿴�����Ƿ�����
        System.out.println("���� ��������: " + jedis.ping());
    }
    @Test
    //Redis Java String(�ַ���) ʵ��
    public void TestRedisString(){
        //���ӱ��ص� Redis ����
          Jedis jedis = new Jedis("localhost");
          System.out.println("Connection to server sucessfully");
          //���� redis �ַ�������
//          jedis.set("runoobkey", "Redis tutorial");
//         // ��ȡ�洢�����ݲ����
//         System.out.println("Stored string in redis:: "+ jedis.get("runoobkey"));
         String name = jedis.get("theName");
         System.out.println("Stored theName in redis:: "+ name);
    }
    
    
}