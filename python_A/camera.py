#!/usr/bin/env python3
"""Project A: RealSense camera capture, image processing, and process observation."""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import pyrealsense2 as rs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Use an Intel RealSense camera, display raw/grayscale/contour "
            "views, and save the unprocessed color stream to MP4."
        )
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("raw_capture.mp4"),
        help="Output path for the unprocessed camera video.",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=640,
        help="RealSense color width.",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="RealSense color height.",
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="RealSense color FPS.",
    )

    return parser.parse_args()


def create_writer(
    path: Path,
    width: int,
    height: int,
    fps: float,
) -> cv2.VideoWriter:
    path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(path),
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        raise RuntimeError(
            "Could not create the MP4 writer. "
            "Check the output path and OpenCV video codec support."
        )

    return writer


def process_frame(
    frame: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Create grayscale and contour views from a color frame."""

    # 彩色图像 -> 灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 先进行高斯模糊，减少噪声
    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0,
    )

    # Canny 边缘检测
    edges = cv2.Canny(
        blurred,
        70,
        140,
    )

    # 查找轮廓
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    # 在原始彩色图像上绘制轮廓
    contour_view = frame.copy()

    cv2.drawContours(
        contour_view,
        contours,
        -1,
        (0, 255, 0),
        2,
    )

    return gray, contour_view


def print_runtime_context(
    args: argparse.Namespace,
) -> None:
    print("=" * 64)
    print("ROBOCON Vision Assignment 1 - Python Project A")
    print(f"PID:          {os.getpid()}")
    print(f"PPID:         {os.getppid()}")
    print(f"Python:       {sys.executable}")
    print(f"Python ver.:  {sys.version.split()[0]}")
    print(f"Camera:       Intel RealSense")
    print(f"Resolution:   {args.width}x{args.height}")
    print(f"FPS:          {args.fps}")
    print(f"Raw output:   {args.output.resolve()}")
    print()
    print("Keep this process running and inspect it from another terminal.")
    print("Press q or ESC in an OpenCV window to exit.")
    print("=" * 64)
    print(flush=True)


def main() -> int:
    args = parse_args()

    print_runtime_context(args)

    # ------------------------------------------------------------
    # 1. 创建 RealSense pipeline
    # ------------------------------------------------------------

    pipeline = rs.pipeline()
    config = rs.config()

    # 我们的 Project A 只需要彩色摄像头。
    config.enable_stream(
        rs.stream.color,
        args.width,
        args.height,
        rs.format.bgr8,
        args.fps,
    )

    writer: Optional[cv2.VideoWriter] = None

    frame_count = 0
    start_time = time.monotonic()

    try:
        # --------------------------------------------------------
        # 2. 启动 RealSense
        # --------------------------------------------------------

        profile = pipeline.start(config)

        print("RealSense started successfully.", flush=True)

        # 获取实际的视频配置
        color_profile = (
            profile
            .get_stream(rs.stream.color)
            .as_video_stream_profile()
        )

        actual_fps = color_profile.fps()

        print(
            f"Actual stream: "
            f"{color_profile.width()}x{color_profile.height()}, "
            f"FPS={actual_fps}",
            flush=True,
        )

        # --------------------------------------------------------
        # 3. 持续读取摄像头
        # --------------------------------------------------------

        while True:

            # 等待下一组 RealSense 帧
            frames = pipeline.wait_for_frames()

            # 获取彩色帧
            color_frame = frames.get_color_frame()

            if not color_frame:
                continue

            # RealSense frame -> NumPy array
            frame = np.asanyarray(
                color_frame.get_data()
            )

            # ----------------------------------------------------
            # 4. 第一次获得有效图像后创建视频写入器
            # ----------------------------------------------------

            if writer is None:

                height, width = frame.shape[:2]

                writer = create_writer(
                    args.output,
                    width,
                    height,
                    actual_fps,
                )

                print(
                    f"Video writer initialized: "
                    f"{width}x{height} @ {actual_fps} FPS",
                    flush=True,
                )

            # ----------------------------------------------------
            # 5. 保存原始图像
            # ----------------------------------------------------

            # 注意：
            # 这里保存的是没有经过灰度化、
            # 边缘检测、轮廓绘制的原始彩色图像。
            writer.write(frame)

            frame_count += 1

            # ----------------------------------------------------
            # 6. 图像处理
            # ----------------------------------------------------

            gray, contour_view = process_frame(frame)

            # ----------------------------------------------------
            # 7. 显示三个窗口
            # ----------------------------------------------------

            cv2.imshow(
                "Project A - Original",
                frame,
            )

            cv2.imshow(
                "Project A - Grayscale",
                gray,
            )

            cv2.imshow(
                "Project A - Contours",
                contour_view,
            )

            # ----------------------------------------------------
            # 8. 检测退出按键
            # ----------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                break

    except KeyboardInterrupt:
        print("\nInterrupted by Ctrl+C.")

    except Exception as exc:
        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        return 1

    finally:

        # --------------------------------------------------------
        # 9. 释放资源
        # --------------------------------------------------------

        pipeline.stop()

        if writer is not None:
            writer.release()

        cv2.destroyAllWindows()

    # ------------------------------------------------------------
    # 10. 输出运行统计
    # ------------------------------------------------------------

    elapsed = max(
        time.monotonic() - start_time,
        1e-6,
    )

    print()
    print("=" * 64)
    print("Project A finished.")
    print(f"Saved raw video: {args.output.resolve()}")
    print(f"Captured frames: {frame_count}")
    print(f"Elapsed time:    {elapsed:.1f} s")
    print(
        f"Loop rate:       "
        f"{frame_count / elapsed:.1f} frame/s"
    )
    print("=" * 64)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())