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
    private String path;

    @RequestMapping(path = "/startpage")
    public ModelAndView gotoStartPage() {
        return new ModelAndView("start_page");
    }

    @RequestMapping(path = "/receivestatisticfile")
    public ModelAndView receiveStatisticFile(
            @RequestParam("statisticFile") MultipartFile statisticFile, HttpServletRequest request) {
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

        ModelAndView modelAndView = new ModelAndView("select_img_type");
        modelAndView.addObject("uploadPath", uploadPath);
        modelAndView.addObject("fileName", fileName);
        return modelAndView;
    }

    @RequestMapping(path = "/confirmimgtype")
    public ModelAndView confirmImgType(String imgType, String pythonDir, String uploadPath, String fileName) {
        switch (imgType) {
            case "relation_plot": {
                ModelAndView modelAndView = new ModelAndView("relation_plot_select_cols");
                modelAndView.addObject("pythonDir", pythonDir);
                modelAndView.addObject("uploadPath", uploadPath);
                modelAndView.addObject("fileName", fileName);
                return modelAndView;
            }
            case "heat_map": {
                ModelAndView modelAndView = new ModelAndView("heat_map_select_cols");
                modelAndView.addObject("pythonDir", pythonDir);
                modelAndView.addObject("uploadPath", uploadPath);
                modelAndView.addObject("fileName", fileName);
                return modelAndView;
            }
            case "stream_plot": {
                ModelAndView modelAndView = new ModelAndView("stream_plot_select_cols");
                modelAndView.addObject("pythonDir", pythonDir);
                modelAndView.addObject("uploadPath", uploadPath);
                modelAndView.addObject("fileName", fileName);
                return modelAndView;
            }
            default: {
                ModelAndView modelAndView = new ModelAndView("quiver_plot_select_cols");
                modelAndView.addObject("pythonDir", pythonDir);
                modelAndView.addObject("uploadPath", uploadPath);
                modelAndView.addObject("fileName", fileName);
                return modelAndView;
            }
        }
    }

    @RequestMapping(path = "/drawrelationplot")
    public ModelAndView drawRelationPlot(String uploadPath, String fileName,
                                         String pythonDir, String col1, String col2) {
        try {
            String relationPlotPy = pythonDir + "\\relation_plot.py";
            String[] pyArgs = new String[]{"python", relationPlotPy, uploadPath, fileName, col1, col2};
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

        ModelAndView modelAndView = new ModelAndView("relation_plot_display");
        modelAndView.addObject("filePath", uploadPath + "/" + fileName);
        return modelAndView;
    }

    @RequestMapping(path = "/displayrelationplot", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayRelationPlot() throws IOException {
        File imgFile = new File(path + "\\relation_plot.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/drawheatmap")
    public ModelAndView drawHeatMap(String uploadPath, String fileName,
                                    String pythonDir, String col1, String col2, String col3) {
        try {
            String heatMapPy = pythonDir + "\\heat_map.py";
            String[] pyArgs = new String[]{"python", heatMapPy, uploadPath, fileName, col1, col2, col3};
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

        return new ModelAndView("heat_map_display");
    }

    @RequestMapping(path = "/displayheatmap", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayHeatMap() throws IOException {
        File imgFile = new File(path + "\\heat_map.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/drawstreamplot")
    public ModelAndView drawStreamPlot(String uploadPath, String fileName,
                                       String pythonDir, String col1, String col2) {
        try {
            String streamPlotPy = pythonDir + "\\stream_plot.py";
            String[] pyArgs = new String[]{"python", streamPlotPy, uploadPath, fileName, col1, col2};
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

        return new ModelAndView("stream_plot_display");
    }

    @RequestMapping(path = "/displaystreamplot", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayStreamPlot() throws IOException {
        File imgFile = new File(path + "\\stream_plot.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }

    @RequestMapping(path = "/drawquiverplot")
    public ModelAndView drawQuiverPlot(String uploadPath, String fileName,
                                       String pythonDir, String col1, String col2) {
        try {
            String quiverPlotPy = pythonDir + "\\quiver_plot.py";
            String[] pyArgs = new String[]{"python", quiverPlotPy, uploadPath, fileName, col1, col2};
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

        return new ModelAndView("quiver_plot_display");
    }

    @RequestMapping(path = "/displayquiverplot", produces = MediaType.IMAGE_PNG_VALUE)
    @ResponseBody
    public byte[] displayQuiverPlot() throws IOException {
        File imgFile = new File(path + "\\quiver_plot.png");
        InputStream inputStream = new FileInputStream(imgFile);
        byte[] bytes = new byte[inputStream.available()];
        inputStream.read(bytes, 0, inputStream.available());
        inputStream.close();
        return bytes;
    }
}
