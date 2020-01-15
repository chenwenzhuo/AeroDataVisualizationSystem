package com.example.AeroDataVisualizationSystem.controller;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import java.io.*;

@Controller
@RequestMapping(path = "/aero")
public class PagesController {
    private String path;//用于保存文件上传路径，在显示图片时使用

    @RequestMapping(path = "/startpage")
    public ModelAndView gotoStartPage() {
        return new ModelAndView("start_page");//返回主页
    }

    @RequestMapping(path = "/receive_statistic_file")
    public ModelAndView receiveStatisticFile(@RequestParam("statisticFile") MultipartFile statisticFile,
                                             String dataSource, String pythonDir, HttpServletRequest request) {
        //上传文件路径
        String uploadPath = request.getServletContext().getRealPath("");
        //文件名
        String fileName = statisticFile.getOriginalFilename();

        System.out.println("File upload path: " + uploadPath);
        try {
            if (!statisticFile.isEmpty()) {
                File filePath = new File(uploadPath, fileName);

                //判断路径是否存在，如果不存在就创建一个
                if (!filePath.getParentFile().exists()) {
                    filePath.getParentFile().mkdirs();
                }
                //将上传文件保存到一个目标文件当中
                statisticFile.transferTo(new File(uploadPath + File.separator + fileName));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        path = uploadPath;

        //根据数据的类型，跳转到不同页面
        ModelAndView modelAndView = new ModelAndView();
        switch (dataSource) {
            case "Burgers":
                modelAndView.setViewName("burgers_select_img_type");
                break;
            case "NS":
                modelAndView.setViewName("ns_select_img_type");
                break;
            case "M6":
                modelAndView.setViewName("m6_relation_select_cols");
                break;
        }
        //传参
        modelAndView.addObject("uploadPath", uploadPath);
        modelAndView.addObject("fileName", fileName);
        modelAndView.addObject("pythonDir", pythonDir);
        return modelAndView;
    }

    @RequestMapping(path = "/draw_burgers")
    public ModelAndView drawBurgersFigure(String imgType, String pythonDir, String uploadPath, String fileName) {
        ModelAndView modelAndView = new ModelAndView();
        String pyFile;
        //根据所需图像的类型，使用不同的python文件，并设置要跳转的页面
        if (imgType.equals("relation")) {
            pyFile = pythonDir + "\\relation_burg.py";
            modelAndView.setViewName("burgers_display_relation");
        } else {
            pyFile = pythonDir + "\\heat_burg.py";
            modelAndView.setViewName("burgers_display_heat");
        }

        try {
            String[] pyArgs = new String[]{"python", pyFile, uploadPath, fileName};

            Process proc = Runtime.getRuntime().exec(pyArgs);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return modelAndView;
    }

    @RequestMapping(path = "/display_burgers_relation", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayBurgersRelation() throws IOException {
        File imgFile = new File(path + "relation_burg.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/display_burgers_heat", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayBurgersHeat() throws IOException {
        File imgFile = new File(path + "heat_burg.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/ns")
    public ModelAndView nsFigure(String imgType, String pythonDir, String uploadPath, String fileName) {
        //若要画折线图，跳转到下一个页面，输入数据列
        if (imgType.equals("relation")) {
            ModelAndView modelAndView = new ModelAndView("ns_relation_select_cols");
            modelAndView.addObject("pythonDir", pythonDir);
            modelAndView.addObject("uploadPath", uploadPath);
            modelAndView.addObject("fileName", fileName);
            return modelAndView;
        }

        //若要画热力图，跳转到下一个页面，输入数据列
        if (imgType.equals("heat")) {
            ModelAndView modelAndView = new ModelAndView("ns_heat_select_cols");
            modelAndView.addObject("pythonDir", pythonDir);
            modelAndView.addObject("uploadPath", uploadPath);
            modelAndView.addObject("fileName", fileName);
            return modelAndView;
        }

        //若要画流场图，无需额外参数，直接调用python作图
        ModelAndView modelAndView = new ModelAndView("ns_display_stream");
        String pyFile = pythonDir + "\\stream_ns.py";

        try {
            String[] pyArgs = new String[]{"python", pyFile, uploadPath, fileName};

            Process proc = Runtime.getRuntime().exec(pyArgs);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return modelAndView;
    }

    @RequestMapping(path = "/draw_ns_relation")
    public ModelAndView drawNSRelation(String pythonDir, String uploadPath, String fileName, int col1, int col2) {
        //取fileName的最后三个字符（文件后缀名）
        int fileNameLen = fileName.length();
        String suffix = fileName.substring(fileNameLen - 3, fileNameLen);

        ModelAndView modelAndView = new ModelAndView();
        String pyFile;
        if (suffix.equals("csv")) {
            pyFile = pythonDir + "\\relation_ns_csv.py";
            modelAndView.setViewName("ns_display_csv_relation");
        } else {
            pyFile = pythonDir + "\\relation_ns_history_dat.py";
            modelAndView.setViewName("ns_display_history_dat_relation");
        }

        try {
            String[] pyArgs = new String[]{"python", pyFile, uploadPath, fileName,
                    String.valueOf(col1), String.valueOf(col2)};

            Process proc = Runtime.getRuntime().exec(pyArgs);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return modelAndView;
    }

    @RequestMapping(path = "/draw_ns_heat")
    public ModelAndView drawNSRHeat(String pythonDir, String uploadPath, String fileName, int title_col) {
        String pyFile = pythonDir + "\\heat_ns.py";
        try {
            String[] pyArgs = new String[]{"python", pyFile, uploadPath, fileName, String.valueOf(title_col)};

            Process proc = Runtime.getRuntime().exec(pyArgs);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return new ModelAndView("ns_display_heat");
    }

    @RequestMapping(path = "/display_ns_csv_relation", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayNSCsvRelation() throws IOException {
        File imgFile = new File(path + "relation_ns_csv.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/display_ns_history_dat_relation", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayNSHistoryDatRelation() throws IOException {
        File imgFile = new File(path + "relation_ns_history_dat.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/display_ns_heat", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayNSHeat() throws IOException {
        File imgFile = new File(path + "heat_ns.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/display_ns_stream", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayNSStream() throws IOException {
        File imgFile = new File(path + "stream_ns.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/draw_m6_relation")
    public ModelAndView drawM6Relation(String uploadPath, String fileName, String pythonDir, String col1, String col2) {
        String pyFile = pythonDir + "\\relation_m6_his_dat.py";
        try {
            String[] pyArgs = new String[]{"python", pyFile, uploadPath, fileName,
                    String.valueOf(col1), String.valueOf(col2)};

            Process proc = Runtime.getRuntime().exec(pyArgs);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ModelAndView("m6_display_relation");
    }

    @RequestMapping(path = "/display_m6_relation", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayM6Relation() throws IOException {
        File imgFile = new File(path + "relation_m6_his_dat.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }
}
