# Hướng dẫn Roblox Manager

Bản Parallel có tên chương trình `Roblox Manager.exe` và tiêu đề cửa sổ `Roblox Manager`. Mục đích là chạy cùng bản gốc trên một máy Windows, với cấu hình và danh sách tài khoản riêng theo thư mục. Tên và định dạng các tệp dữ liệu được giữ nguyên để có thể sao chép tài khoản từ bản gốc.

## 1. Build trên Windows

1. Chép toàn bộ cây mã nguồn `ram-parallel` sang Windows; giữ nguyên cấu trúc thư mục và tệp `Launcher.cs` ở thư mục gốc của solution.
2. Cài **Visual Studio 2022**. Trong Visual Studio Installer, chọn workload **.NET desktop development**. Cài thêm **.NET Framework 4.7.2 targeting pack / Developer Pack** nếu Visual Studio báo thiếu framework đích.
3. Mở tệp **`RBX Alt Manager.sln`** bằng Visual Studio 2022.
4. Trong Solution Explorer, nhấp chuột phải vào solution và chọn **Restore NuGet Packages**. Đợi quá trình tải/khôi phục các package hoàn tất.
5. Chọn cấu hình **Release**, nền tảng **Any CPU**, rồi chọn **Build > Build Solution**. Có thể dùng cấu hình Release/x86 sẵn có nếu cần.
6. Sau khi build thành công, chương trình chính nằm tại **`build\Release\Roblox Manager.exe`**, tính từ thư mục chứa solution. Build cũng tạo launcher tương thích `build\Release\RBX Alt Manager.exe`, trỏ đến EXE Parallel.

Nếu NuGet hoặc framework còn thiếu, xử lý thông báo trong Build Output rồi build lại. Bản mã nguồn này mới được kiểm tra trên Linux; chưa được biên dịch hoặc chạy thử trên Windows.

## 2. Cài vào thư mục RIÊNG

Ví dụ dùng hai thư mục:

| Phiên bản | Thư mục ví dụ |
| --- | --- |
| Bản gốc | `Desktop\RAM-Original` |
| Parallel | `Desktop\RAM-Parallel` |

Chép **toàn bộ nội dung** của `build\Release` vào `Desktop\RAM-Parallel`, gồm EXE, tệp cấu hình và các thư mục/thư viện phụ được tạo khi build. Không chỉ chép riêng EXE, và không giải nén/chép đè vào thư mục bản gốc.

Chạy `Roblox Manager.exe` trong thư mục Parallel. Nếu tạo shortcut, mở **Properties** và đặt:

- **Target:** đường dẫn đầy đủ đến `Roblox Manager.exe` trong thư mục Parallel.
- **Start in:** đường dẫn đầy đủ đến chính thư mục `RAM-Parallel`.

Shortcut của bản gốc cũng cần **Start in** trỏ về thư mục bản gốc. Nếu chạy bằng terminal hoặc công cụ tự khởi động, đặt working directory tương ứng với từng bản. Chương trình đọc/ghi dữ liệu theo `Environment.CurrentDirectory`; chỉ tách đường dẫn EXE mà dùng chung working directory thì vẫn có thể dùng chung dữ liệu. Nếu dùng mục tự khởi động của ứng dụng, kiểm tra thư mục thực tế mà ứng dụng tạo dữ liệu sau khi đăng nhập lại Windows.

## 3. Hai bản hoạt động cùng nhau thế nào?

Hai bản có mutex ứng dụng khác nhau. Vì vậy có thể mở một cửa sổ bản gốc và một cửa sổ Parallel cùng lúc; bản Parallel vẫn chặn việc mở thêm chính nó trong bản build Release. Tên sản phẩm khác nhau cũng tách tên mục khởi động cùng Windows trong Registry.

Mỗi thư mục làm việc lưu riêng `RAMSettings.ini`, `AccountData.json`, `RecentGames.json`, `RAMTheme.ini` và các dữ liệu cục bộ khác. Thêm/xóa tài khoản hoặc đổi theme/cấu hình ở một bản không tự đồng bộ sang bản kia khi hai working directory được đặt đúng.

| Chức năng | Cổng mặc định bản gốc | Cổng mặc định Parallel |
| --- | --- | --- |
| HTTP Web Server / `RAMAccount.lua` | `7963` | `7964` |
| Nexus WebSocket | `5242` | `5243` |

Web Server chỉ mở khi được bật trong cài đặt; Nexus mở khi khởi chạy chức năng tương ứng. Dùng `RAMAccount.lua` đi kèm bản Parallel cho cổng `7964`. Nexus của Parallel dùng `localhost:5243`, kể cả loader được xuất từ giao diện Parallel. Nếu tự đổi cổng, cập nhật cả cài đặt lẫn host/port trong script sử dụng; hai bản phải dùng cổng khác nhau. Loader Nexus xuất từ giao diện mặc định ghi rõ cổng `5243`, nên cần sửa host trong loader nếu dùng cổng tùy chỉnh.

## 4. Chuyển tài khoản từ bản gốc

1. Thoát cả hai chương trình để tránh tệp bị ghi trong lúc sao chép.
2. Sao lưu `AccountData.json` của bản gốc và của Parallel nếu Parallel đã có tài khoản.
3. Sao chép **chỉ tệp `AccountData.json`** từ thư mục dữ liệu bản gốc sang thư mục `RAM-Parallel`. Có thể ghi đè tệp cùng tên sau khi đã sao lưu; thao tác này thay danh sách hiện tại của Parallel, không gộp hai danh sách.
4. Mở lại Parallel bằng đúng thư mục làm việc. Nếu dữ liệu được bảo vệ bằng mật khẩu, nhập mật khẩu cũ.

Thực hiện trên **cùng máy PC**, nên dùng cùng tài khoản Windows như bản gốc để giữ điều kiện giải mã dữ liệu hiện có. Cơ chế mã hóa và định dạng tệp không bị thay đổi. Đây là sao chép dữ liệu tại một thời điểm; các thay đổi về sau ở hai bản được lưu riêng.

**KHÔNG chép `RAMSettings.ini` từ bản gốc.** Tệp đó có thể mang theo cổng `7963`/`5242` và bật lại kiểm tra cập nhật, gây xung đột hoặc mất bản Parallel. Hãy để Parallel tự tạo cấu hình mới, rồi chỉnh các tùy chọn cần thiết trong giao diện.

## 5. Multi Roblox

Có thể bật **Multi Roblox** trong **một trong hai ứng dụng** trước khi mở Roblox. Chỉ cần một ứng dụng giữ mutex chung `ROBLOX_singletonMutex`; không bắt buộc bật cả hai. Giữ ứng dụng đó chạy trong lúc cần chức năng này.

Nếu bản gốc đã giữ mutex, Parallel sẽ giữ thêm handle của chính nó và coi Multi Roblox là đã bật, thay vì báo lỗi vì không giành được quyền sở hữu. Khi tắt tính năng, Parallel chỉ đóng handle của mình, không gọi `ReleaseMutex` để thả mutex do ứng dụng khác sở hữu.

Nếu muốn bật trong **cả hai**, hãy mở/bật ở **bản gốc trước**, sau đó mở/bật ở Parallel, rồi mới chạy Roblox. Bản gốc không được sửa nên vẫn có thể hiện cảnh báo cũ nếu bật Multi Roblox ở bản gốc sau khi Parallel đã sở hữu mutex. Có thể tránh trường hợp đó bằng cách chỉ bật trong một bản. Nên mở lần lượt hai ứng dụng; mã gốc còn có thao tác kiểm tra/khóa tệp cookie Roblox lúc khởi động.

Các thao tác vốn tác động đến toàn bộ tiến trình Roblox, như đóng tất cả cửa sổ, quy tắc watcher hoặc sửa cài đặt client Roblox, vẫn giữ nguyên. Nếu sao chép cùng một tài khoản sang hai bản, tùy chọn tự đóng phiên trước (`AutoCloseLastProcess`) có thể đóng phiên Roblox mà bản kia vừa mở cho tài khoản đó. Hai bộ dữ liệu riêng không tạo ra hai môi trường Roblox cách ly.

## 6. Giữ cập nhật tự động TẮT

Trong Parallel, giữ **Settings > Check for Updates** ở trạng thái **OFF / không đánh dấu**. Giá trị mặc định mới là `CheckForUpdates=false`, nhưng vẫn cần kiểm tra nếu đang dùng cấu hình có sẵn.

**Không bấm Force Update và không chạy với tham số `-update` trong Parallel.** Bộ cập nhật gốc vẫn được giữ nguyên và tải release của dự án gốc; nó không phải bộ cập nhật dành cho Parallel. Nó có thể thay các tệp Parallel bằng bản gốc, đồng thời còn chứa thao tác theo tên tiến trình/shortcut gốc. Muốn cập nhật Parallel, dùng mã nguồn Parallel đã được kiểm tra rồi build và triển khai lại vào đúng thư mục riêng.

## 7. Kiểm tra sau khi build

- Mở lần lượt bản gốc và Parallel; xác nhận hai cửa sổ cùng tồn tại và Parallel có tiêu đề `(Parallel)`.
- Kiểm tra hai bộ tệp dữ liệu nằm trong hai thư mục riêng; giữ **Check for Updates** tắt ở Parallel.
- Nếu sử dụng Web Server/Nexus, bật chức năng ở cả hai và xác nhận mỗi script kết nối đến đúng cổng trong bảng trên. Nếu báo cổng bận, kiểm tra cổng đã lưu trong INI và chương trình khác đang chiếm cổng.
- Bật Multi Roblox theo thứ tự hướng dẫn ở trên trước khi mở Roblox; thử tắt/đóng Parallel trong khi bản gốc vẫn giữ mutex để xác nhận bản gốc tiếp tục hoạt động.
- Kiểm tra danh sách tài khoản đã sao chép và chức năng khởi chạy trên máy Windows của bạn.

Chưa có kết quả build Windows, kiểm thử mutex/Registry/cổng thực tế hoặc giải mã dữ liệu trên máy của chủ sở hữu từ môi trường Linux này. Chi tiết thay đổi từng tệp nằm trong `CHANGES.md`.
